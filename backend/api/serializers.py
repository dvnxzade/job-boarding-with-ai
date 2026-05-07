from .models import Application , Job
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"