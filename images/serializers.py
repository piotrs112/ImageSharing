from images.models import Image, UserPlan
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()

    def get_plan_name(self, user) -> str:
        return UserPlan.objects.get(user=user).plan.name

    class Meta:
        model = User
        fields = ['username', 'plan_name']
        read_only = True
        many = False


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['owner']
