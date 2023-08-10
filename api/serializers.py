from rest_framework import serializers
from .models import ImageDocument, PDFDocument

FILE_TYPES = (
    ('img', 'Image'),
    ('pdf', 'PDF'),
)

class ImageDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageDocument
        fields = '__all__'
        extra_kwargs = {
            'file': {'write_only': True},
            'height': {'read_only': True},
            'width': {'read_only': True},
            'number_of_channels': {'read_only': True},
        }


class PDFDocSerializer(serializers.ModelSerializer):

    class Meta:
        model = PDFDocument
        fields = '__all__'
        extra_kwargs = {
            'file': {'write_only': True},
            'number_of_pages': {'read_only': True},
            'pages_info': {'read_only': True},
        }

class DocumentUploadSerializer(serializers.Serializer):
    # To be implemented
    pass