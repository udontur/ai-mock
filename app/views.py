from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('input_file')
        if uploaded_file:
            # Process the uploaded file (e.g., save it, analyze it, etc.)
            # For now, just return a success message
            return render(request, 'index.html', {'message': 'File uploaded successfully!'})
        else:
            return render(request, 'index.html', {'error': 'No file uploaded.'})
    return render(request, 'index.html')
