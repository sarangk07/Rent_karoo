from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


# Create your models here.


class MyAccountManager(BaseUserManager):
    
    def create_user(self,first_name ,last_name ,username, email ,password=None):#Information about the user|| The user's password, which defaults to None to allow for users without a password (e.g., social media logins).

        if not email :
            raise ValueError('User must have an email address')
        #The method checks if email and username are provided. If not, it raises ValueError with a message indicating that an email address and username are required.
        if not username:
            raise ValueError('User must have an username') 
        
        user = self.model(#self.model= it's an attribute that you define in your custom manager to specify the user model associated with that manager
            email = self.normalize_email(email), #enter any capital letter email the  normalize_email make to smalletter
            username = username,
            first_name = first_name,
            last_name = last_name,  
        )
        user.set_password(password)#making hashed password
        user.save(using = self._db)
        # print(user.password)
        return user
    
        
    
    def create_superuser(self,first_name ,last_name ,username, email ,password):
          user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
          # superuser permitions
          user.is_admin = True
          user.is_staff = True
          user.is_active =True
          user.is_superuser = True
          # user.is_superadmin = True
          user.save(using=self._db ) # _db save the database or db connection
          return user


class Registerinfo(AbstractBaseUser):
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)

    # requre fileds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' # we can able to login with email in username field  or username insted of email
    REQUIRED_FIELDS = ['username','first_name'  ,'last_name',] 
    
    
    objects = MyAccountManager()
    
    
    class Meta:
        verbose_name = 'registerinfo'
        verbose_name_plural = 'users'
    
    
 
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):# a person is_admin he can all permitons to change everything 
        return self.is_admin
    
    def has_module_perms(self,add_label):# Check if the user has the appropriate permissions for the module
        return True











