from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

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
    username = models.CharField(max_length=50, unique=True)
    phone_number = PhoneNumberField(region='KG')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Group(Group):
    name = models.CharField(max_length=30)
    description = models.TextField()
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    group_picture = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class GroupMembers(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    members = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'
