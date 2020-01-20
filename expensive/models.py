from autoslug import AutoSlugField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from django.db import models


class UserType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ExtendedUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, null=True, default=None)
    type = models.ForeignKey(UserType, null=True, default=None, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='get_full_name', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class TransactionType(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Source(models.Model):
    source = models.CharField(max_length=50)

    def __str___(self):
        return self.source


class Transaction(models.Model):
    owner = models.ForeignKey(ExtendedUser, related_name='transactions', on_delete=models.CASCADE)
    source = models.ForeignKey(Source, related_name="transactions", on_delete=models.CASCADE)
    transaction_date = models.DateField()
    post_date = models.DateField()
    amount = models.FloatField()
    description = models.TextField()
    type = models.ManyToManyField(TransactionType, related_name='transaction')
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id