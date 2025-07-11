from django.shortcuts import render
import fitz # PyMuPDF
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from os import getenv

def read_file(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def parse_text(text):
    template = """
    You are a helpful assistant. Please summarize the following text: {text}
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template
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
