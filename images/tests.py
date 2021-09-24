from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class TestImageModel(TestCase):
    def setUp(self) -> None:
        User.objects.create(username="basic_user")
        User.objects.create(username="premium_user")
        User.objects.create(username="enterprise_user")
