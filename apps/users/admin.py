from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from apps.users.models import User, Department


@admin.register(User)
class UserAdmin(UserAdmin):
    pass

admin.site.register(Department)
