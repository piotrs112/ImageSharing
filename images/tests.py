import os
from PIL import Image as PIL_Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from images.models import ExpiringLink, Image, Plan, UserPlan


class TestImageModel(TestCase):
    def setUp(self) -> None:
        basic = User()
        basic.username = "basic"
        basic.set_password("basic")
        basic.save()
        UserPlan.objects.create(
            user=basic, plan=Plan.objects.get(name="Basic"))

        premium = User()
        premium.username = "premium"
        premium.set_password("premium")
        premium.save()
        UserPlan.objects.create(
            user=premium, plan=Plan.objects.get(name="Premium"))

        enterprise = User()
        enterprise.username = "enterprise"
        enterprise.set_password("enterprise")
        enterprise.save()
        UserPlan.objects.create(
            user=enterprise, plan=Plan.objects.get(name="Enterprise"))

    def test_thumbnail_generation(self):
        """
        Create image, add to database and check generated thumbnail sizes
        """
        blank_image = PIL_Image.new(mode="RGB", size=(2000, 1000), color=(255,255,255))
        blank_image.save('test_image.jpg')


        img = Image()
        img.owner = User.objects.get(username="premium")
        img.image = SimpleUploadedFile(name='test_image.jpg', content=open('test_image.jpg', 'rb').read(), content_type='image/jpeg')
        img.save()

        thumbnail_200 = PIL_Image.open('uploads/200/test_image.jpg')
        self.assertEqual(thumbnail_200.height, 200)

        thumbnail_400 = PIL_Image.open('uploads/400/test_image.jpg')
        self.assertEqual(thumbnail_400.height, 400)

    def tearDown(self):
        """
        Cleanup
        """
        super().tearDown()
        print("\nDeleting temporary files\n")
        os.remove("test_image.jpg")
        os.remove("uploads/test_image.jpg")
        os.remove("uploads/400/test_image.jpg")
        os.remove("uploads/200/test_image.jpg")


class TestPlanModel(TestCase):
    def setUp(self) -> None:
        self.user = User()
        self.user.username = "test_user"
        self.user.save()

    def test_default_plans(self) -> None:
        """
        Test default plans migration
        """
        basic = Plan.objects.get(name="Basic")
        self.assertEqual(basic.original_file_link, False)
        self.assertEqual(basic.expiring_link, False)

        premium = Plan.objects.get(name="Premium")
        self.assertEqual(premium.original_file_link, True)
        self.assertEqual(premium.expiring_link, False)

        enterprise = Plan.objects.get(name="Enterprise")
        self.assertEqual(enterprise.original_file_link, True)
        self.assertEqual(enterprise.expiring_link, True)

    def test_init(self) -> None:
        """
        Test correct object init and save in db
        """
        plan = Plan()
        plan.name = "test_plan"
        plan.expiring_link = True
        plan.original_file_link = False
        plan.save()

        plan = Plan.objects.get(pk=plan.pk)

        self.assertEqual(plan.name, "test_plan")
        self.assertEqual(plan.expiring_link, True)
        self.assertEqual(plan.original_file_link, False)

    def test_str(self) -> None:
        """
        Test if str() returns plan name
        """
        plan = Plan.objects.create(
            name="test", expiring_link=True, original_file_link=False)
        self.assertEqual(str(plan), plan.name)


class TestExpiringLinkModel(TestCase):
    def setUp(self) -> None:
        return

    def test_init(self):
        link = ExpiringLink()