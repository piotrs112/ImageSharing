import os
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from PIL import Image as PIL_Image

from images.models import Image, ImageHeight, UserPlan

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

@receiver(post_delete, sender=Image)
def delete_thumbnails(sender, instance, **kwargs):
    """
    Delete thumbnails when original file is deleted
    """
    #todo

@receiver(pre_save, sender=ImageHeight)
def create_image_size_folder(sender, instance, **kwargs):
    path = f"uploads/{instance.height}"
    if not os.path.isdir(path):
        os.mkdir(path)