from django.contrib.auth.models import User
from images.models import ExpiringLink, Image, ImageHeight, Plan, UserPlan
from django.contrib import admin


class ImageHeightInlineAdmin(admin.StackedInline):
    model = ImageHeight

class PlanAdmin(admin.ModelAdmin):
    model = Plan
    inlines = [ImageHeightInlineAdmin]

class UserPlanInline(admin.StackedInline):
    model = UserPlan

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [UserPlanInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Image)
admin.site.register(ImageHeight)
admin.site.register(Plan, PlanAdmin)
admin.site.register(ExpiringLink)