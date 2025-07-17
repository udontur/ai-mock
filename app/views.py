from django.shortcuts import render

from app.modules import parser

def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('input_file')
        if uploaded_file:
            raw_latex = parser.pdf_to_raw_latex(uploaded_file)
            parsed_text = parser.parse_raw_latex(raw_latex)
            return render(request, 'index.html', {'message': 'File processed successfully.', 'parsed_text': parsed_text})
        else:
            return render(request, 'index.html', {'error': 'No file uploaded.'})
    return render(request, 'index.html')

