from django.shortcuts import render
import pymupdf
import os

from app.modules import llm

def pdf_to_raw_latex(pdf_file):
    doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

    # Use Nougat?
    raw_latex = ""

    doc.close()
    return raw_latex

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
