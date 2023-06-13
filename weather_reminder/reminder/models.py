from celery.utils.time import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, IntegrityError


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, is_staff=False, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        if User.objects.filter(email=self.normalize_email(email).lower()).exists():
            raise ValueError('This email has already been registered.')

        user = self.model(
            email=self.normalize_email(email).lower(),
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        user.set_password(password)
        try:
            user.save(using=self._db)

        except IntegrityError:
            raise ValueError('This email has already been registered.')

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "This email has already been registered.",
        }
    )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'reminder'


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_weather_request = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    PERIOD_CHOICES = [
        (1, '1 hours'),
        (3, '3 hours'),
        (6, '6 hours'),
        (12, '12 hours'),
    ]
    period = models.IntegerField(choices=PERIOD_CHOICES)
    last_notification_sent = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.user.name} - {self.city.name}'


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    weather_conditions = models.CharField(max_length=255)
    feels_like = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.city} - {self.timestamp}'
