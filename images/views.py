import os
from http.client import HTTPResponse

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import response
from django.http.response import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from images.models import ExpiringLink, Image, ImageHeight, UserPlan
from images.serializers import ExpiringLinkSerializer, ImageSerializer, UserSerializer


class ImageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        new_image = Image.objects.create(owner=request.user, image=data["image"])
        new_image.save()
        serializer = self.serializer_class(new_image)
        return Response(serializer.data, status=HTTP_201_CREATED)

    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpiringLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ExpiringLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpiringLink.objects.filter(image__owner=self.request.user)


def get_image(request, pk, height=None):
    """
    Serve image if user is owner and has access to requested size
    """
    image = get_object_or_404(Image, pk=pk)
    if image.owner == request.user:
        plan = UserPlan.objects.get(user=request.user).plan

        folder, filename = os.path.split(image.image.file.name)

        if height is None and plan.original_file_link:
            return FileResponse(image.image, as_attachment=True)

        elif height in [ih.height for ih in ImageHeight.objects.filter(plan=plan)]:
            path = os.path.join(folder, str(height), filename)
            path = os.path.relpath(path)
            return FileResponse(open(path, "rb"), as_attachment=True)

        else:
            raise Http404
    else:
        raise PermissionDenied


def get_image_from_filename(request, filename, _height=None):
    """
    Serve image based on filename
    """
    _pk = Image.objects.get(image=f"uploads/{filename}").pk
    return get_image(request, _pk, _height)


def get_image_from_exlink(request, hashid):
    exlink = ExpiringLink.objects.get(hashid=hashid)
    if not exlink.is_expired():
        return get_image(
            request, exlink.image.id, exlink.height.height
        )  # FIXME: should be available for all
    else:
        return JsonResponse({"error": "link expired"})
