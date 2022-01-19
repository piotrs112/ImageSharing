from datetime import datetime
from typing import Literal, Union
from urllib import request

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from images.models import ExpiringLink, Image, UserPlan


class UserSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()

    def get_plan_name(self, user) -> str:
        return UserPlan.objects.get(user=user).plan.name

    class Meta:
        model = User
        fields = ["username", "plan_name"]
        read_only = True
        many = False


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ["owner"]


class ExpiringLinkSerializer(serializers.ModelSerializer):
    exlink = serializers.SerializerMethodField()

    def get_exlink(self, exlink):
        return reverse(
            "exlink-image", args=[exlink.hashid], request=self.context["request"]
        )

    class Meta:
        model = ExpiringLink
        exclude = ["hashid"]
