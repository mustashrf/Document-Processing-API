from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
import base64
from django.core.files.base import ContentFile
from PIL import Image
import io

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

def encode_img(img):
    img.show()
    buffered = io.BytesIO()
    img.save(buffered, format="png")
    encoded_img = base64.b64encode(buffered.getvalue())
    return encoded_img

def rotate_img(instance, rotation_angle):
    img = Image.open(instance.file)
    rotated_img = img.rotate(rotation_angle, expand=True)
    return encode_img(rotated_img)

def convert_pdf_to_img(instance):
    pdf_file = fitz.open(instance.file.path)
    encoded_images_list = []
    for page_num, page in enumerate(pdf_file):
        pix = page.get_pixmap()
        encoded_img = encode_img(Image.frombytes("RGB", [pix.width, pix.height], pix.samples))
        encoded_images_list.append({
            'page_number':page_num + 1,
            'image': encoded_img
        })
    return encoded_images_list

class DocumentProcessingView(APIView):
    def post(self, request):
        serializer = DocumentProcessingSerializer(data=request.data)
        if serializer.is_valid():
            path = request.path
            id = request.data['id']

            if 'rotate' in path:
                rotation_angle = float(request.data.get('rotation_angle'))
                if rotation_angle is None:
                    return Response({'error': 'Please provide the rotation angle.'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    instance = ImageDocument.objects.get(id=id)
                    rotated_img = rotate_img(instance, rotation_angle)
                    return Response({'rotated_image':rotated_img}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error':f'{e}'}, status=status.HTTP_404_NOT_FOUND)

            elif 'convert-pdf-to-image' in path:
                try:
                    instance = PDFDocument.objects.get(id=id)
                    encoded_images = convert_pdf_to_img(instance)
                    return Response({'encoded_images': encoded_images}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error':f'{e}'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)