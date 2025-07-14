from django.shortcuts import render
import fitz # PyMuPDF
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from os import getenv

def read_file(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        current_page_text=page.get_text()
        text += current_page_text
        print(f"[Extracted question from page {page.number+1}]")
        try:
            extracted_questions=parse_text(current_page_text).content
        except:
            print(f"Failed to parse page {page.number+1}, trying for the 2nd time")
            try:
                extracted_questions=parse_text(current_page_text).content               
            except:
                print(f"Failed to parse page {page.number+1}, trying for the 3rd time")
                try:
                                extracted_questions=parse_text(current_page_text).content
                except:
                    print(f"Failed to parse page {page.number+1}!")
                    extracted_questions="PARSE_ERROR"
                    
        print(extracted_questions)
        print(f"[End of extracted question from page {page.number+1}]\n")
    doc.close()
    return text

def parse_text(text):
    input_prompt = """
        You are an expert assistant tasked with accurately extracting exam questions from the provided university exam text. Follow these instructions precisely:
        Extract only the full text of each question, including any problem descriptions, context, and the question itself, exactly as it appears in the input.
        Preserve all mathematical expressions, formatting them properly using LaTeX syntax.
        Do not include any additional commentary, answers, explanations, scores, or information beyond the extracted questions.
        Separate each extracted question with exactly one blank line, each individual question should be on the same line.
        Each question should not be numbered. 
        Your response must not contain non-ASCII characters. All responses must only contain ASCII characters. 
        If the input contains no questions, respond with the exact text: "No questions found.".
        If a question appears incomplete or truncated, respond with the exact text: "Incomplete question.".
        Adhere strictly to these rules to ensure clarity and accuracy.
        The following is the given text:
        {text}
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template = input_prompt
    )
    llm = ChatOpenAI(
        openai_api_key = getenv('OPENROUTER_API_KEY'),
        openai_api_base = getenv('OPENROUTER_API_BASE'),
        model_name = getenv('OPENROUTER_MODEL_NAME'),
    )
    llm_chain = prompt | llm
    response = llm_chain.invoke(input={'text': text})
    return response

def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('input_file')
        if uploaded_file:
            # Get the text of the uploaded file
            text = read_file(uploaded_file)
            
            # Pass the text to the LLM
            response = parse_text(text)
            return render(request, 'index.html', {'message': 'File processed successfully.', 'text': text, 'response': response.content})
        else:
            return render(request, 'index.html', {'error': 'No file uploaded.'})
    return render(request, 'index.html')
