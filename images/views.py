import os
from django.http.response import HttpResponse
from images import serializers
from images.serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from images.models import Image, ImageHeight, UserPlan


class ImageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

def get_image(request, pk, height=None) -> HttpResponse:
    image = Image.objects.get(pk=pk)
    if image.owner == request.user:
        plan = UserPlan.objects.get(user=request.user).plan
        serializer = ImageSerializer(image)
        if height is None and plan.original_file_link:
            return HttpResponse(serializer.data)

        elif height in [ih.height for ih in ImageHeight.objects.filter(plan=plan)]:
           folder, filename = os.path.split(serializer.data['image'])
           _data = serializer.data
           _data['image'] = os.path.join(folder, str(height), filename)
           return HttpResponse(_data)
        
        else:
            return HttpResponse({'error': 'You dont have permissions to do this'})
    else:
        return HttpResponse(f"errror")
