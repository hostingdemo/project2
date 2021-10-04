from django.core.validators import MaxLengthValidator, MinLengthValidator, ValidationError
# from django.core import ValidationError
from django.db import models
from django.utils import timezone
from datetime import datetime    
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.conf import settings
from schools.models import *

User = settings.AUTH_USER_MODEL

class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=None):
        """
        Creates and saves a User with the given email.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        if is_staff:
            user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email.
        """
        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_admin', True)
        # other_fields.setdefault('is_active', True)

        user = self.create_user(email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    def validate_digit_length(self, phone):
        if not (phone.isdigit() and len(phone) == 10):    
            raise ValidationError('%(phone)s must be 10 digits', params={'phone': phone},)

    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    mobile_no = models.CharField(max_length=10, validators=[validate_digit_length], default='0', blank=True)
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'


class emails_record(models.Model):
    to = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.now, blank=True)
