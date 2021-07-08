from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('user must have an email address')
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name= last_name,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self.db)
        return user

class Accounts(AbstractBaseUser):
    choices = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    department = models.CharField(max_length=50)
    photo = models.ImageField(default='default.png')
    occupation = models.CharField(max_length=20, choices=choices)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
    