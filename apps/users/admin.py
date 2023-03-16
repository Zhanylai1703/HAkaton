from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from apps.users.models import User, Department


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar', 'role')

admin.site.register(Department)
