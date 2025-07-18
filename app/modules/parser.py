from django.shortcuts import render
import pymupdf
import os

from app.modules import llm
from app.modules import prompt

def pdf_to_raw_latex(pdf_file):
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

    # Use Nougat?
    raw_latex = ""

    doc.close()
    return raw_latex

def parse_raw_latex(raw_latex):
    input_prompt = prompt.prompt_parse_raw_latex
    llm_response = llm.get_response(user_prompt=input_prompt, text=raw_latex)
    return llm_response
