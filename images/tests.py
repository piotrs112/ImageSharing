from images.models import Plan, UserPlan
from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class TestImageModel(TestCase):
    def setUp(self) -> None:
        basic = User()
        basic.username = "basic"
        basic.set_password("basic")
        basic.save()
        UserPlan.objects.create(user=basic, plan=Plan.objects.get(name="Basic"))

        premium = User()
        premium.username = "premium"
        premium.set_password("premium")
        premium.save()
        UserPlan.objects.create(user=premium, plan=Plan.objects.get(name="Premium"))

        enterprise = User()
        enterprise.username = "enterprise"
        enterprise.set_password("enterprise")
        enterprise.save()
        UserPlan.objects.create(user=enterprise, plan=Plan.objects.get(name="Enterprise"))