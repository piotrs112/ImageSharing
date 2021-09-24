from django.db import migrations


def create_default_plans(apps, schema_editor):
    """
    Create 3 default plans: Basic, Premium, Enterprise
    """
    ImageHeight = apps.get_model('images', 'ImageHeight')
    Plan = apps.get_model('images', 'Plan')

    # Basic plan
    basic_plan = Plan()
    basic_plan.name = "Basic"
    basic_plan.original_file_link = False
    basic_plan.expiring_link = False
    basic_plan.save()

    im_h_200_basic = ImageHeight()
    im_h_200_basic.height = 200
    im_h_200_basic.plan = basic_plan
    im_h_200_basic.save()

    # Premium plan
    premium_plan = Plan()
    premium_plan.name = "Premium"
    premium_plan.original_file_link = True
    basic_plan.expiring_link = False
    premium_plan.save()

    im_h_200_premium = ImageHeight()
    im_h_200_premium.height = 200
    im_h_200_premium.plan = premium_plan
    im_h_200_premium.save()

    im_h_400_premium = ImageHeight()
    im_h_400_premium.height = 400
    im_h_400_premium.plan = premium_plan
    im_h_400_premium.save()

    # Enterprise plan
    enterprise_plan = Plan()
    enterprise_plan.name = "Enterprise"
    enterprise_plan.original_file_link = True
    enterprise_plan.expiring_link = True
    enterprise_plan.save()

    im_h_200_enterprise = ImageHeight()
    im_h_200_enterprise.height = 200
    im_h_200_enterprise.plan = enterprise_plan
    im_h_200_enterprise.save()

    im_h_400_enterprise = ImageHeight()
    im_h_400_enterprise.height = 400
    im_h_400_enterprise.plan = enterprise_plan
    im_h_400_enterprise.save()


class Migration(migrations.Migration):
    dependencies = [
        ('images', '0001_initial')
    ]

    operations = [
        migrations.RunPython(create_default_plans)
    ]
