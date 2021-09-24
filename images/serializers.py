from images.models import Image
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'plan']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['owner']