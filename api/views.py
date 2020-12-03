from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from api.models import FileProcessing, FileProcessingSerializer, FileProcessingUploadSerializer
from api.tasks import find_data


class FileProcessingStatus(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FileProcessing.objects.all()
    serializer_class = FileProcessingSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_processing_create(request):
    if request.method == 'POST':
        serializer = FileProcessingUploadSerializer(data=request.data)
        if serializer.is_valid():
            res_id = serializer.save()
            find_data.delay(res_id.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

