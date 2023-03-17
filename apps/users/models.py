from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)

ROLE_CHOICES = (
    ('DEV', 'DEV'),
    ('PM', 'PM'),
    ('QA', 'QA'),
    ('BA', 'BA'),
)

class User(AbstractUser):
    password2 = models.CharField(max_length=25)
    is_moderator = models.BooleanField(
        default=False, verbose_name='Это модератор'
    )
    email= models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='profile_images', 
        blank=True, null=True)
    role = models.CharField(
        choices=ROLE_CHOICES, max_length=20)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=50)
    user =  models.ManyToManyField(
        'User', related_name='dep_users', blank=True) 
    

    def add_user(self, user, admin):
        if admin.is_superuser:
            self.users.add(user)
        else:
            raise Exception('Добавлять пользователей в группу может только администратор')

    
    def __str__(self):
        return self.name

