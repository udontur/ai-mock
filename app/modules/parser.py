from django.shortcuts import render
import fitz
import os

from app.modules import llm
from app.modules import prompt

def get_latex_pdf(pdf_file):
    """Convert a PDF file to raw LaTeX format.

    Args:
        pdf_file: The PDF file to convert.

    Returns:
        str: The raw LaTeX representation of the PDF.
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    # TODO: Find a package that can convert PDF to LaTeX directly
    # Currently, we are just extracting text as a placeholder
    raw_latex = get_text_pdf(pdf_file)

    doc.close()
    return raw_latex

def parse_raw_latex(raw_latex):
    """Parse raw LaTeX text and extract the questions.

    Args:
        raw_latex (str): The raw LaTeX text to parse.

    Returns:
        BaseMessage: The questions extracted from the raw LaTeX text.
    """
    input_prompt = prompt.prompt_parse_raw_latex
    llm_response = llm.get_response(user_prompt=input_prompt, text=raw_latex)
    return llm_response

def get_text_pdf(pdf_file):
    """Get the text content from a text-based PDF file.

    Args:
        pdf_file: The PDF file to extract text from.

    Returns:
        str: The text content of the PDF.
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def get_image_pdf(pdf_file):
    """Get the text content from an image-based PDF file.

    Args:
        pdf_file: The PDF file to extract images from.

    Returns:
        str: The text content of the PDF.
    """
    return get_text_pdf(pdf_file)  # Placeholder for image extraction logic
