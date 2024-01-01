from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# from home.models import Cars


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        # print(user.password)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        # superuser permitions
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_superadmin = True
        user.save(using=self._db)  # _db save the database or db connection
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
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    objects = MyAccountManager()

    class Meta:
        verbose_name = "registerinfo"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.email}"

    # def __str__(self):
    #     return f"{self.email}" if self.email else f"{self.username}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Profile(models.Model):
    GENDER = [
        ("M", "M"),
        ("F", "F"),
        ("TRANS", "TRANS"),
    ]

    user = models.OneToOneField(
        Registerinfo,
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=100, null=True)
    mobile = PhoneNumberField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    age = models.IntegerField(null=True)
    education = models.CharField(max_length=50, null=True)
    licencePhoto = models.ImageField(
        upload_to="media/userimages", null=True, blank=True
    )
    state = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=40, null=True)
    profilePic = models.ImageField(upload_to="media/userimages", null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile Update"

    def __str__(self):
        return f"{self.user}  {self.mobile}"
