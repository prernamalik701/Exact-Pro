# # myapp/views.py

# import os  # Import the os module

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Document
# from .summary_generator import generate_pdf_summary  # Import the function

# class UploadPDFAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         file = request.FILES.get('pdf')
#         # Process the uploaded file here (e.g., save to database)
#         document = Document(file=file)
#         document.save()
        
#         # Define the output PDF path
#         BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the base directory of the Django project
#         output_pdf_path = os.path.join(BASE_DIR, 'pdf_summaries', 'summary.pdf')  # Specify the path for saving the PDF
        
#         # Generate summary using AI model
#         summary = generate_pdf_summary(file, output_pdf_path)  # Call the function
        
#         if summary:
#             return Response({"message": "File uploaded successfully", "summary": summary}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "Error generating summary"}, status=status.HTTP_400_BAD_REQUEST)
        
          
       # myapp/views.py

import os  # Import the os module
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .utils import generate_summary  # Import your function to generate the summary

class UploadPDFAPIView(APIView):
    @staticmethod
    @csrf_exempt
    def upload_pdf(request):
        if request.method == 'POST':
            # Get the uploaded PDF file from the request
            uploaded_file = request.FILES.get('pdf')

            if not uploaded_file:
                return Response({'error': 'No PDF file provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Save the uploaded PDF file to a temporary location
                # You can save it to a temporary directory or process it directly
                document = Document.objects.create(file=uploaded_file)

                # Generate summary using your AI model
                summary = generate_summary(document.file.path)  # Pass the path of the uploaded file to your function

                # Return the summary in the API response
                return Response({"message": "File uploaded successfully", "summary": summary}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            # Return an error response for other HTTP methods
            return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
