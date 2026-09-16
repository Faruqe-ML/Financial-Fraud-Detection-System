from django.db import models
from django.contrib.auth.hashers import make_password


class Registration(models.Model):

    full_name = models.CharField(max_length=150)

    date_of_birth = models.DateField()

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, blank=True)

    address = models.TextField(blank=True)

    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.full_name

