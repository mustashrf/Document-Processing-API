from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name="document_upload_view"),

    path('images/', ImageDocumentView.as_view(), name="image_list_view"),
    path('images/<int:pk>', ImageDocumentView.as_view(), name="image_detail_delete_view"),
    path('pdfs/', PDFDocumentView.as_view(), name="pdf_list_view"),
    path('pdfs/<int:pk>', PDFDocumentView.as_view(), name="pdf_detail_delete_view"),

    path('rotate/', DocumentProcessingView.as_view(), name="image-rotate"),
    path('convert-pdf-to-image/', DocumentProcessingView.as_view(), name="pdf-conversion"),
]
