from django.db import models
from rest_framework import serializers


class FileProcessing(models.Model):
    filename = models.FileField(upload_to="file_upload")
    date_time_upload = models.DateTimeField(auto_now_add=True)
    date_time_end = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, null=True)
    result = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.filename.name


class FileProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileProcessing
        fields = ("filename", "date_time_upload", "date_time_end", "status", "result")


class FileProcessingUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileProcessing
        fields = ("id", "filename")
