from django.shortcuts import render
import pymupdf
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
import io
import subprocess
from PIL import Image
import requests
import time
from fastapi import UploadFile, File

nougat_url_root="http://127.0.0.1:8503/"

def wait_for_nougat_to_start(timeout):
    for current_second in range(1..30):
        try:
            response = requests.post(nougat_url_root)
            print("[AI-MOCK]: The NOUGAT server is running.")
            return
        except requests.exceptions.RequestException:
            pass
        print(f"[AI-MOCK]: Elapsed {current_second.number} seconds: Starting NOUGAT server...")
        time.sleep(1)

def nougat_pdf_to_markdown(file) -> str:
    #pdf_bytes = doc.write()
    #pdf_buffer = io.BytesIO(pdf_bytes)
    content=file.read()
    headers = {
        "content-type": "application/pdf"
    }
    fastapi_file = UploadFile(filename=file.name, file=io.BytesIO(content), headers=headers)
    print("Started nougat")
    nougat_api_url = "http://127.0.0.1:8503/predict/"
    nougat_files = {
        "file": (file.name, fastapi_file, "application/pdf")
    }
    nougat_headers = {
        "accept": "application/json"
    }
    nougat_predicted_text = requests.post(nougat_api_url, nougat_files, nougat_headers)
    print(nougat_predicted_text.json())
    
def read_parse_file(file):
    wait_for_nougat_to_start(timeout=30)
    pdf_text=nougat_pdf_to_markdown(file)
    print("[PDF TEXT]")
    print(pdf_text)
    print("[END  END]")
    # for page in doc:
    #     # pil_image = pdf_to_pil_image(page)
    #     # current_page_text = latex_ocr_model(pil_image)
    #     #pix.save(f"page{page.number+1}.png")
    #     # convert PDF to PNG byte
    #     # image_byte = image_pixmap.pil_tobytes(format="PNG", dpi=(300, 300))
    #     # Open the PNG byte
    #     # image = Image.open(BytesIO(image_byte))
    #     # Pass the PNG to LatexOCR
    #     #image = Image.open(f"page{page.number+1}.png")
    #     print(f"[STR Extracted questions from page {page.number+1}]")
    #     print(current_page_text)
        # print(f"[END Extracted questions from page {page.number+1}]")
    # doc.close()
# def read_file(file):
#     doc = fitz.open(stream=file.read(), filetype="pdf")
#     text = ""
#     for page in doc:
#         current_page_text=page.get_text()
#         print(f"[PDF raw text from page {page.number+1}]")
#         print(current_page_text)
#         print(f"[End of PDF raw text from page {page.number+1}]")
#         text += current_page_text
#         print(f"[Extracted question from page {page.number+1}]")
#         try:
#             extracted_questions=parse_text(current_page_text).content
#         except:
#             print(f"Failed to parse page {page.number+1}, trying for the 2nd time")
#             try:
#                 extracted_questions=parse_text(current_page_text).content               
#             except:
#                 print(f"Failed to parse page {page.number+1}, trying for the 3rd time")
#                 try:
#                     extracted_questions=parse_text(current_page_text).content
#                 except:
#                     print(f"Failed to parse page {page.number+1}!")
#                     extracted_questions="PARSE_ERROR"
                    
#         print(extracted_questions)
#         print(f"[End of extracted question from page {page.number+1}]\n")
#     doc.close()
#     return text

# def parse_text(text):
#     input_prompt = """
#         You are an expert assistant tasked with accurately extracting exam questions from the provided university exam text. Follow these instructions precisely:
#         Extract only the full text of each question, including any problem descriptions, context, and the question itself, exactly as it appears in the input.
#         Preserve all mathematical expressions, formatting them properly using LaTeX syntax.
#         Do not include any additional commentary, answers, explanations, scores, or information beyond the extracted questions.
#         Separate each extracted question with exactly one blank line, each individual question should be on the same line.
#         Each question should not be numbered. 
#         Your response must not contain non-ASCII characters. All responses must only contain ASCII characters. 
#         If the input contains no questions, respond with the exact text: "No questions found.".
#         If a question appears incomplete or truncated, respond with the exact text: "Incomplete question.".
    #     Adhere strictly to these rules to ensure clarity and accuracy.
    #     The following is the given text:
    #     {text}
    # """
    # prompt = PromptTemplate(
    #     input_variables=["text"],
    #     template = input_prompt
    # )
    # llm = ChatOpenAI(
    #     openai_api_key = getenv('OPENROUTER_API_KEY'),
    #     openai_api_base = getenv('OPENROUTER_API_BASE'),
    #     model_name = getenv('OPENROUTER_MODEL_NAME'),
    # )
    # llm_chain = prompt | llm
    # response = llm_chain.invoke(input={'text': text})
    # return response

async def nougat_api():
    subprocess.Popen(["nougat_api"])

def index(request):
    return render(request, 'index.html')

async def upload_file(request):
    await nougat_api()
    if request.method == 'POST':
        uploaded_file = request.FILES.get('input_file')
        if uploaded_file:
            all_parsed= read_parse_file(uploaded_file)
            # Get the text of the uploaded file
            # text = read_file(uploaded_file)
            # # Pass the text to the LLM
            # response = parse_text(text)
            return render(request, 'index.html', {'message': 'File processed successfully.', 'parsed_text': all_parsed})
        else:
            return render(request, 'index.html', {'error': 'No file uploaded.'})
    return render(request, 'index.html')
