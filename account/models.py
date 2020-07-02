from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, name, phone, password = None):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")
        if not phone:
            raise ValueError("User must have a phone")
            
        user = self.model(
                email = self.normalize_email(email),
                name = name,
                phone = phone,
            )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, email, name, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
    phone = models.CharField(max_length = 30, unique = True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length = 30)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'name']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.phone
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def set_phone(self, phone):
        self.phone = phone
        return True
    
    def set_name(self, name):
        self.name = name
        return True
    
    def set_email(self, email):
        self.email = email
        return True