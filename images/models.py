import os
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models.deletion import CASCADE

USER_MODEL = get_user_model()


def get_basic_plan():
    return Plan.objects.get_or_create(name="Basic")[0]


class UserPlan(models.Model):
    """
    Model storing user plan information
    """

    user = models.OneToOneField(User, on_delete=CASCADE)
    plan = models.ForeignKey("Plan", on_delete=models.PROTECT, default=get_basic_plan)


class Image(models.Model):
    """
    Model implementing image storage and manipulation
    """

    image = models.ImageField(
        upload_to="uploads/", validators=[FileExtensionValidator(["jpg", "png"])]
    )
    owner = models.ForeignKey(
        USER_MODEL, verbose_name="image_owner", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Returns image filename
        """
        return os.path.basename(self.image.file.name)


class Plan(models.Model):
    """
    Model implementing user plans
    """

    name = models.CharField(max_length=64, verbose_name="plan_name")
    original_file_link = models.BooleanField("Show original file link")
    expiring_link = models.BooleanField("Enable expiring links")

    def __str__(self) -> str:
        return self.name


class ImageHeight(models.Model):
    """
    Image height model for setting available thumbnail heights in plans
    """

    height = models.IntegerField("image_height")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.height}px for plan {self.plan.name}"


class ExpiringLink(models.Model):
    """
    Model implementing expiring links
    """

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    time = models.PositiveIntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        if datetime.now() > self.expiration_datetime():
            return True
        else:
            return False

    def expiration_datetime(self) -> datetime:
        return self.timestamp + timedelta(seconds=self.time)

    def __str__(self) -> str:
        return f"Link to {self.image}. Expires at {self.expiration_datetime()}."
