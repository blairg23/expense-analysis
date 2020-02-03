from autoslug import AutoSlugField
from autoslug.utils import slugify
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from django.db import models


class UserType(models.Model):
    name = models.TextField(choices=(('admin', 'Administrator'), ('developer', 'Developer')), unique=True)
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
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.first_name + ' ' + self.last_name)
        return super(ExtendedUser, self).save(*args, **kwargs)


class TransactionType(models.Model):
    transaction_type = models.TextField(choices=(
        ('debit', 'Debit'),
        ('credit', 'Credit'),
        ('expense', 'Expense'),
        ('payment', 'Payment'),
        ('income', 'Income'),
        ('fee', 'Fee')
    ), unique=True)
    description = models.CharField(max_length=50)
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_type


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50)
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category


class Source(models.Model):
    source = models.TextField()#(choices=(('capitalone', 'Capital One'), ('citi', 'Citi'), ('chase', 'Chase'), ('discover', 'Discover')), unique=True)
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.source


class Transaction(models.Model):
    owner = models.ForeignKey(ExtendedUser, related_name='transactions', on_delete=models.CASCADE)
    source = models.ForeignKey(Source, related_name="transactions", on_delete=models.CASCADE)
    transaction_date = models.DateField()
    post_date = models.DateField()
    amount = models.FloatField()
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='transactions')
    accounting_type = models.ForeignKey(TransactionType, related_name='accounting_transactions', on_delete=models.DO_NOTHING)
    semantic_type = models.ForeignKey(TransactionType, related_name='semantic_transactions', on_delete=models.DO_NOTHING)
    # Administrative Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source} - {self.transaction_date} - {self.amount} - {self.description}"
