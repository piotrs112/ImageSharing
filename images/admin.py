from django.contrib.auth.models import User
from images.models import ExpiringLink, Image, ImageHeight, Plan, UserPlan
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class ImageHeightInlineAdmin(admin.StackedInline):
    model = ImageHeight


class PlanAdmin(admin.ModelAdmin):
    model = Plan
    inlines = [ImageHeightInlineAdmin]


class UserPlanInline(admin.StackedInline):
    model = UserPlan


class CustomUserAdmin(UserAdmin):
    model = User
    inlines = [UserPlanInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Image)
admin.site.register(ImageHeight)
admin.site.register(Plan, PlanAdmin)
admin.site.register(ExpiringLink)
