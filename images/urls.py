from django.urls.conf import include, path, re_path
from rest_framework import routers
from images import views

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet, basename="Images")
router.register(r'user', views.UserViewSet, basename="User")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'), name='api-auth'),
    #re_path(r'^uploads/[0-9A-z\_\.]+$', views.get_image_from_filename),
    path('uploads/<str:filename>/', views.get_image_from_filename, name='get-original'),
    path('uploads/<str:filename>/<int:_height>/', views.get_image_from_filename, name='get-thumbnail')
]