from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

class DocumentUploadView(APIView):
    # To be implemented
    pass

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

