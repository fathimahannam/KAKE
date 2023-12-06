from django.db import models

# from Baker.models import Cake

# Create your models here.

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserAccountManager(BaseUserManager):
    
    def _create_user(self,email,password,**extra_fields):
       if not email:
            raise ValueError('Your have not provided a valid e-mail address')
       
       email=self.normalize_email(email)
       user=self.model(email=email,**extra_fields)
       user.set_password(password)
       user.save(using=self._db)     
       return user
    

    def create_user(self, email=None, password=None, **extra_fields):
      
        return self._create_user(email, password, **extra_fields)
        
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_active',True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)




    

        

    

class UserAccount(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255,default="Unnamed")
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserAccountManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def _str_(self):
        return self.email
    # def __str__(self):
    #     return str(self.id)
    
class Address(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user.id)
   
class Transaction(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    datetime = models.DateTimeField(auto_now_add=True)

    def _str_(self) -> str:
        return str(self.id)



