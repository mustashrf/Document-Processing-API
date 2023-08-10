from django.db import models
import os
from PIL import Image
import fitz

class ImageDocument(models.Model):
    file = models.ImageField(upload_to='images')
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    number_of_channels = models.IntegerField(blank=True)

    def __str__(self):
        return (self.file.name.split('/'))[-1]

    def save(self, *args, **kwargs):
        image = Image.open(self.file)
        self.width = image.width
        self.height = image.height
        self.number_of_channels = len(image.getbands())
        super().save(*args, **kwargs)

class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs')
    number_of_pages = models.IntegerField(null=True, blank=True)
    pages_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return (self.file.name.split('/'))[-1]

    def save(self, *args, **kwargs):
        with open('temp_pdf', 'wb') as temp_pdf:
            temp_pdf.write(self.file.read())
            temp_pdf_path = temp_pdf.name
        
        doc = fitz.open(temp_pdf_path)

        number_of_pages = len(doc)

        pages_info_list = []
        for page_num, page in enumerate(doc):
            page_width = page.rect.width
            page_height = page.rect.height
            page_info = {
                'page_num': page_num + 1,
                'width': page_width,
                'height': page_height
            }
            pages_info_list.append(page_info)
        
        doc.close()
        os.remove(temp_pdf_path)

        self.number_of_pages = number_of_pages
        self.pages_info = pages_info_list

        super().save(*args, **kwargs)