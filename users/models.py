from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import json
from django.core.serializers.json import DjangoJSONEncoder
from works.models import Company, Schedule, Sphere, Experience, Employment, Currency
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    avatar = models.ImageField(
        null=True, blank=True, upload_to='avatars', default="avatars/icons8-avatar-96.png")
    birth_date = models.DateField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_all_companies(self):
        companies = Company.objects.all()
        return companies

    def get_all_schedules(self):
        schedules = Schedule.objects.all()
        return schedules

    def get_all_spheres(self):
        spheres = Sphere.objects.all()
        return spheres

    def get_all_experiences(self):
        experiences = Experience.objects.all()
        return experiences

    def get_all_employments(self):
        employments = Employment.objects.all()
        return employments

    def get_all_currencies(self):
        currencies = Currency.objects.all()
        return currencies

    def get_absolute_url(self):
        return reverse('user-profile', args=[self.id])
