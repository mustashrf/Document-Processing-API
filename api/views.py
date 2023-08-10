from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
import base64
from django.core.files.base import ContentFile

class DocumentUploadView(APIView):
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_type = serializer.data['file_type']
            base64_data = serializer.data['base64_data']
            try:
                decoded_data = base64.b64decode(base64_data)
                content_file = ContentFile(decoded_data, name=f'uploaded.{"png" if file_type=="img" else "pdf"}')

                file_data = {'file': content_file}

                if file_type == 'img':
                    serializer = ImageDocSerializer(data=file_data)
                else:
                    serializer = PDFDocSerializer(data=file_data)

                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDocumentView(generics.GenericAPIView):
    queryset = ImageDocument.objects.all()
    serializer_class = ImageDocSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                instance = self.get_queryset().get(pk=pk)
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except:
                return Response('Not found!', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer =  self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data)
    
    def delete(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Not found!', status=status.HTTP_404_NOT_FOUND)


class PDFDocumentView(generics.GenericAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                instance = self.get_queryset().get(pk=pk)
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except:
                return Response('Not found!', status=status.HTTP_404_NOT_FOUND)
        else:
            serializer =  self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data)
    
    def delete(self, request, pk):
        instance = self.get_queryset().get(pk=pk)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Not found!', status=status.HTTP_404_NOT_FOUND)

def rotate_img():
    pass

def convert_pdf_to_img():
    pass

def encode_img():
    pass

class DocumentProcessingView(APIView):
    def post(self, request):
        path = request.path
        id = request.data['id']
        if 'rotate' in path:
            rotation_angle = request.data.get('rotation_angle') or None
            if rotation_angle is None:
                return Response('Please provide the rotation angle.', status=status.HTTP_400_BAD_REQUEST)
            # rotate image
        elif 'convert-pdf-to-image' in path:
            # convert_pdf_to_image
            pass
        serializer = DocumentProcessingSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
        return Response('OK')