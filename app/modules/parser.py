from django.shortcuts import render
import pymupdf
import os
import re
import json

from app.modules import llm

def extract_mathematical_content(text):
    """
    Identify potential mathematical content in text that might need LaTeX conversion.
    Returns a list of tuples: (original_text, start_pos, end_pos, math_type)
    """
    math_patterns = [
        # Common mathematical expressions
        (r'\b(?:sin|cos|tan|log|ln|exp|sqrt|sum|integral?|derivative|limit)\s*\([^)]+\)', 'function'),
        # Fractions like a/b, (x+1)/(y-2), etc.
        (r'\([^)]+\)\s*/\s*\([^)]+\)', 'fraction'),
        # Powers and subscripts like x^2, a_i, etc.
        (r'\w+[\^_]\{?[^}\s]+\}?', 'power_subscript'),
        # Greek letters spelled out
        (r'\b(?:alpha|beta|gamma|delta|epsilon|theta|lambda|mu|pi|sigma|omega|phi|psi|chi)\b', 'greek'),
        # Mathematical operators and symbols
        (r'(?:≤|≥|≠|∞|∑|∏|∫|∂|∇|±|×|÷|√)', 'symbol'),
        # Common mathematical notation like derivatives d/dx
        (r'd/d[a-zA-Z]', 'derivative'),
        # Equations with equals
        (r'\w+\s*[=]\s*[^.!?]+', 'equation'),
        # Matrix notation [a b; c d] or similar
        (r'\[[^\]]*;[^\]]*\]', 'matrix'),
        # Integrals notation
        (r'∫[^=]+d[a-zA-Z]', 'integral'),
    ]
    
    math_content = []
    for pattern, math_type in math_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            math_content.append((
                match.group(),
                match.start(),
                match.end(),
                math_type
            ))
    
    # Sort by position and remove overlaps
    math_content.sort(key=lambda x: x[1])
    filtered_content = []
    last_end = 0
    
    for content, start, end, math_type in math_content:
        if start >= last_end:  # No overlap
            filtered_content.append((content, start, end, math_type))
            last_end = end
    
    return filtered_content

def apply_basic_latex_formatting(text):
    """
    Apply basic LaTeX formatting without LLM for common patterns.
    This provides immediate value even when LLM is not available.
    """
    # Common symbol replacements
    symbol_map = {
        '±': r'$\pm$',
        '∞': r'$\infty$',
        '≤': r'$\leq$',
        '≥': r'$\geq$',
        '≠': r'$\neq$',
        '∑': r'$\sum$',
        '∏': r'$\prod$',
        '∫': r'$\int$',
        '∂': r'$\partial$',
        '∇': r'$\nabla$',
        '×': r'$\times$',
        '÷': r'$\div$',
        '√': r'$\sqrt{}$',
        'α': r'$\alpha$',
        'β': r'$\beta$',
        'γ': r'$\gamma$',
        'δ': r'$\delta$',
        'ε': r'$\epsilon$',
        'θ': r'$\theta$',
        'λ': r'$\lambda$',
        'μ': r'$\mu$',
        'π': r'$\pi$',
        'σ': r'$\sigma$',
        'ω': r'$\omega$',
        'φ': r'$\phi$',
        'ψ': r'$\psi$',
        'χ': r'$\chi$',
    }
    
    result = text
    for symbol, latex in symbol_map.items():
        result = result.replace(symbol, latex)
    
    # Basic patterns for common mathematical expressions
    # Power notation: x^2, x^3, etc.
    result = re.sub(r'(\w+)\^(\w+)', r'$\1^{\2}$', result)
    
    # Subscript notation: x_1, x_i, etc.
    result = re.sub(r'(\w+)_(\w+)', r'$\1_{\2}$', result)
    
    # Simple fractions in parentheses
    result = re.sub(r'\(([^)]+)\)/\(([^)]+)\)', r'$\\frac{\1}{\2}$', result)
    
    # Greek letter names to LaTeX (use simple replacement to avoid regex issues)
    greek_replacements = {
        ' alpha ': r' $\alpha$ ',
        ' beta ': r' $\beta$ ',
        ' gamma ': r' $\gamma$ ',
        ' delta ': r' $\delta$ ',
        ' epsilon ': r' $\epsilon$ ',
        ' theta ': r' $\theta$ ',
        ' lambda ': r' $\lambda$ ',
        ' mu ': r' $\mu$ ',
        ' pi ': r' $\pi$ ',
        ' sigma ': r' $\sigma$ ',
        ' omega ': r' $\omega$ ',
        ' phi ': r' $\phi$ ',
        ' psi ': r' $\psi$ ',
        ' chi ': r' $\chi$ ',
    }
    
    for name, latex in greek_replacements.items():
        result = result.replace(name, latex)
        result = result.replace(name.capitalize(), latex)
    
    # Common functions (safer approach)
    function_replacements = {
        'sin(': r'$\sin($',
        'cos(': r'$\cos($',
        'tan(': r'$\tan($',
        'log(': r'$\log($',
        'ln(': r'$\ln($',
        'exp(': r'$\exp($',
        'sqrt(': r'$\sqrt{$',
    }
    
    for func, latex in function_replacements.items():
        result = result.replace(func, latex)
    
    return result

def convert_text_to_latex(text_content, math_content):
    """
    Convert identified mathematical content to LaTeX format using LLM.
    Processes content in chunks to respect token limits.
    """
    if not math_content:
        return text_content
    
    # Group mathematical content by context to process efficiently
    math_chunks = []
    current_chunk = []
    chunk_size = 0
    max_chunk_chars = 2000  # Conservative limit to stay within token constraints
    
    for content, start, end, math_type in math_content:
        # Add context around mathematical content
        context_start = max(0, start - 50)
        context_end = min(len(text_content), end + 50)
        context = text_content[context_start:context_end]
        
        if chunk_size + len(context) > max_chunk_chars and current_chunk:
            math_chunks.append(current_chunk)
            current_chunk = []
            chunk_size = 0
        
        current_chunk.append({
            'original': content,
            'context': context,
            'type': math_type,
            'start': start,
            'end': end
        })
        chunk_size += len(context)
    
    if current_chunk:
        math_chunks.append(current_chunk)
    
    # Process each chunk with LLM
    latex_replacements = {}
    
    for chunk in math_chunks:
        try:
            chunk_prompt = """
Convert the following mathematical expressions to proper LaTeX format. 
For each mathematical expression, provide the LaTeX equivalent.
Keep regular text unchanged, only convert mathematical notation.

Mathematical expressions found:
"""
            for item in chunk:
                chunk_prompt += f"\nType: {item['type']}\nOriginal: {item['original']}\nContext: {item['context']}\n---"
            
            chunk_prompt += """

Respond with a JSON object where keys are the original expressions and values are their LaTeX equivalents.
Example: {"x^2": "$x^2$", "alpha": "$\\alpha$", "sin(x)": "$\\sin(x)$"}
"""
            
            response = llm.get_response(user_prompt=chunk_prompt, text="")
            
            # Parse LLM response
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            # Try to extract JSON from response
            json_match = re.search(r'\{[^}]*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    replacements = json.loads(json_match.group())
                    latex_replacements.update(replacements)
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            # If LLM processing fails, use basic LaTeX formatting
            print(f"LLM processing failed: {e}")
            for item in chunk:
                original = item['original']
                # Basic LaTeX conversion for common cases
                if item['type'] == 'power_subscript':
                    latex_replacements[original] = f"${original}$"
                elif item['type'] == 'greek':
                    latex_replacements[original] = f"$\\{original}$"
                elif item['type'] == 'symbol':
                    latex_replacements[original] = f"${original}$"
                else:
                    latex_replacements[original] = f"${original}$"
    
    # Apply replacements to text
    result_text = text_content
    # Sort replacements by length (longest first) to avoid partial replacements
    sorted_replacements = sorted(latex_replacements.items(), key=lambda x: len(x[0]), reverse=True)
    
    for original, latex in sorted_replacements:
        if latex and latex != original:
            result_text = result_text.replace(original, latex)
    
    return result_text

def pdf_to_raw_latex(pdf_file):
    """
    Extract text from PDF and convert mathematical content to LaTeX format.
    Uses a hybrid approach: PyMuPDF for text extraction + LLM for math conversion.
    """
    try:
        # Handle different types of file objects
        if hasattr(pdf_file, 'read'):
            # Ensure we're at the beginning of the file
            if hasattr(pdf_file, 'seek'):
                pdf_file.seek(0)
            pdf_data = pdf_file.read()
            # Reset file pointer for any subsequent operations
            if hasattr(pdf_file, 'seek'):
                pdf_file.seek(0)
        else:
            # If it's already bytes
            pdf_data = pdf_file
        
        if not pdf_data:
            return "Error: PDF file is empty."
        
        doc = pymupdf.open(stream=pdf_data, filetype="pdf")
        
        if doc.page_count == 0:
            doc.close()
            return "Error: PDF contains no pages."
        
        raw_text = ""
        page_count = min(doc.page_count, 20)  # Limit to first 20 pages to manage resources
        
        for page_num in range(page_count):
            page = doc[page_num]
            
            # Try different extraction methods
            page_text = ""
            
            # Method 1: Standard text extraction
            try:
                page_text = page.get_text()
            except Exception:
                pass
            
            # Method 2: If no text found, try HTML format (preserves more structure)
            if not page_text.strip():
                try:
                    html_text = page.get_text("html")
                    # Basic HTML to text conversion
                    page_text = re.sub(r'<[^>]+>', ' ', html_text)
                    page_text = re.sub(r'\s+', ' ', page_text).strip()
                except Exception:
                    pass
            
            # Method 3: Try dictionary format for detailed structure
            if not page_text.strip():
                try:
                    text_dict = page.get_text("dict")
                    page_text = ""
                    if 'blocks' in text_dict:
                        for block in text_dict['blocks']:
                            if 'lines' in block:
                                for line in block['lines']:
                                    if 'spans' in line:
                                        for span in line['spans']:
                                            if 'text' in span:
                                                page_text += span['text'] + " "
                                        page_text += "\n"
                except Exception:
                    pass
            
            # If still no text, the page might be image-based
            if not page_text.strip():
                page_text = f"[Page {page_num + 1}: Image-based content detected - consider using OCR]\n"
            
            raw_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
        
        doc.close()
        
        if not raw_text.strip():
            return "Error: No text content could be extracted from the PDF."
        
        # Apply basic LaTeX formatting first
        latex_text = apply_basic_latex_formatting(raw_text)
        
        # Identify mathematical content
        math_content = extract_mathematical_content(latex_text)
        
        # Convert additional mathematical content to LaTeX format using LLM if available
        if math_content:
            enhanced_latex = convert_text_to_latex(latex_text, math_content)
            return enhanced_latex
        else:
            # No additional mathematical content found, return with basic formatting
            return latex_text
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error processing PDF: {str(e)}\nDetails: {error_details}"

def parse_raw_latex(raw_latex):
    prompt = """
        You are an expert assistant tasked with accurately extracting exam questions from the provided university exam latex. Follow these instructions precisely:
        Extract only the full latex of each question, including any problem descriptions, context, and the question itself, exactly as it appears in the input.
        Do not include any additional commentary, answers, explanations, scores, or information beyond the extracted questions.
        Separate each extracted question with exactly one blank line, each individual question should be on the same line.
        Each question should not be numbered. 
        Your response must not contain non-ASCII characters. All responses must only contain ASCII characters. 
        If the input contains no questions, respond with the exact text: "No questions found.".
        If a question appears incomplete or truncated, respond with the exact text: "Incomplete question.".
        Adhere strictly to these rules to ensure clarity and accuracy.
        The following is the given text:
    """
    llm_response = llm.get_response(user_prompt=prompt, text=raw_latex)
    return llm_response
