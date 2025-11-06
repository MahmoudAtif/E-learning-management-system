from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, User

# Register your models here.


@admin.register(User)
class CustomeUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_student",
                    "is_instructor",
                ),
            },
        ),
    )


admin.site.register(Student)
# admin.site.register(User)
