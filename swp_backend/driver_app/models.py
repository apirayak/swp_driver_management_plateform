from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
from django.db import models


class Role(models.Model):
    ROLE_CHOICES = (
        ("driver", "Driver"),
        ("operator", "Operator"),
        ("admin", "Admin"),
    )

    role_name = models.CharField(choices=ROLE_CHOICES, max_length=20)
    role_description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(
        verbose_name=("created_date"),
        null=True,
        blank=False,
        auto_now_add=True,
    )
    last_updated_date = models.DateTimeField(
        verbose_name=("last_updated_date"),
        null=True,
        blank=False,
        auto_now=True,
    )

    def __str__(self):
        return self.get_role_name_display()


class Warehouse(models.Model):
    warehouse_name = models.CharField(null=True, blank=False, max_length=100)
    warehouse_address = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(
        verbose_name=("created_date"),
        null=True,
        blank=False,
        auto_now_add=True,
    )
    last_updated_date = models.DateTimeField(
        verbose_name=("last_updated_date"),
        null=True,
        blank=False,
        auto_now=True,
    )

    def __str__(self):
        return str(self.warehouse_name) or "Warehouse {}".format(
            self.warehouse_name
        )


class CustomUserManager(BaseUserManager):
    def create_user(
        self, username, email=None, password=None, role=None, **extra_fields
    ):
        if not username:
            raise ValueError("The Username field must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, role=role, **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=150, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_updated_date = models.DateTimeField(
        verbose_name=("last_updated_date"),
        null=True,
        blank=False,
        auto_now=True,
    )

    role = models.ForeignKey(
        Role, null=True, blank=True, on_delete=models.CASCADE
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.username) or f"User info {self.username}"


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(
        Warehouse, null=True, blank=True, on_delete=models.CASCADE
    )
    id_card_number = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    bank_account = models.TextField(null=True, blank=True)
    car_license = models.TextField(null=True, blank=True)
    id_card_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="image_upload/user_info",
        max_length=511,
    )
    driver_license = models.ImageField(
        null=True,
        blank=True,
        upload_to="image_upload/user_info",
        max_length=511,
    )
    photo_with_card = models.ImageField(
        null=True,
        blank=True,
        upload_to="image_upload/user_info",
        max_length=511,
    )
    profile_photo = models.ImageField(
        null=True,
        blank=True,
        upload_to="image_upload/user_info",
        max_length=511,
    )
    created_date = models.DateTimeField(
        verbose_name=("created_date"),
        null=True,
        blank=False,
        auto_now_add=True,
    )
    last_updated_date = models.DateTimeField(
        verbose_name=("last_updated_date"),
        null=True,
        blank=False,
        auto_now=True,
    )

    def __str__(self):
        return str(self.user.first_name) or "Driver info {}".format(
            self.user.first_name
        )


# Operator Profile Model
class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_location = models.CharField(max_length=255, null=True, blank=True)
    extension_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Operator Profile: {self.user.username}"


# Admin Profile Model
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_level = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Admin Profile: {self.user.username}"
