from django.shortcuts import render

from app.modules import parser
from app.modules import prompt


def index(request):
    prompt.init_prompt()
    return render(request, "index.html")


def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("input_file")
        if uploaded_file:
            match request.POST.get("pdf_type", "Text"):
                case "Text":
                    raw_latex = parser.get_text_pdf(uploaded_file)
                    parsed_text = parser.parse_raw_latex(raw_latex)
                case "Image":
                    raw_latex = parser.get_image_pdf(uploaded_file)
                    parsed_text = parser.parse_raw_latex(raw_latex)
                case "LaTeX":
                    raw_latex = parser.get_latex_pdf(uploaded_file)
                    parsed_text = parser.parse_raw_latex(raw_latex)
            return render(
                request,
                "index.html",
                {"message": "File processed successfully.", "parsed_text": parsed_text},
            )
        else:
            return render(request, "index.html", {"error": "No file uploaded."})
    return render(request, "index.html")
