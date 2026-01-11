from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "preview", "description", "owner")
    list_filter = (
        "name",
        "owner",
    )
    search_fields = ("owner",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "preview",
        "description",
        "owner",
        "video",
        "course",
        "owner",
    )
    list_filter = (
        "name",
        "owner",
    )
    search_fields = ("owner",)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "course",
        "created_at",
        "is_active",
    )
    list_filter = (
        "course",
        "owner",
    )
    search_fields = ("owner",)