from django.contrib import admin
from .models import Users, Blogs
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    model = Users
    list_display = ["email", "name", "profile_picture"]
    # Specify the fieldsets to display in the admin panel
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "username", "profile_picture")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )

    # Specify any fields to exclude from the admin panel
    exclude = ("first_name", "last_name", "date_joined")
    search_fields = ("email",)


class BlogAdmin(admin.ModelAdmin):
    list_display = ["blog_title", "staff_member", "date"]


admin.site.register(Users, UsersAdmin)
admin.site.register(Blogs, BlogAdmin)

# Register your models here.
