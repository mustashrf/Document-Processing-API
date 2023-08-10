from django.contrib import admin
from .models import ImageDocument, PDFDocument

# Register your models here.
admin.site.register(ImageDocument)
admin.site.register(PDFDocument)