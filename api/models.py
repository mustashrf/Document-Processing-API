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


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdfs')
    number_of_pages = models.IntegerField(null=True, blank=True)
    pages_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return (self.file.name.split('/'))[-1]
