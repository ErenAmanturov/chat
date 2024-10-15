from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class Image(models.Model):
    image = models.ImageField(upload_to='users/profile_photo/')


class Manager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone_number must be set!')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=10)
    phone_number = PhoneNumberField(region='KG', unique=True)

    objects = Manager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

