import os
from django.contrib.auth.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image as PIL_Image

from images.models import Image, ImageHeight, Plan, UserPlan


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance, **kwargs):
    """
    Create appropriate thumbnails when image is saved
    """
    image = PIL_Image.open(instance.image.name)

    user_plan = UserPlan.objects.get(user=instance.owner)
    image_heights = ImageHeight.objects.filter(plan=user_plan.plan)

    for image_height in image_heights:
        height = image_height.height
        _image = image.resize((int(image.width*height/image.height), height))
        _image.save(f"uploads/{height}/{instance}")


@receiver(pre_save, sender=ImageHeight)
def create_image_size_folder(sender, instance, **kwargs):
    path = f"uploads/{instance.height}"
    if not os.path.isdir(path):
        os.mkdir(path)

@receiver(post_save, sender=User)
def create_superuserplan_if_not_exists(sender, instance, **kwargs):
    """
    Create userplan for superusers
    """
    try:
        UserPlan.objects.get(user=instance)
    except UserPlan.DoesNotExist:
        if instance.is_superuser:
            plan = Plan.objects.get(name="Enterprise")
            UserPlan.objects.create(user=instance, plan=plan)