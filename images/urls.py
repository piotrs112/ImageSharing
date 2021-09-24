from django.urls.conf import include, path
from rest_framework import routers
from images import views

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet, basename="Images")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('img/<int:pk>/', views.get_image),
    path('img/<int:pk>/<int:height>/', views.get_image),
]