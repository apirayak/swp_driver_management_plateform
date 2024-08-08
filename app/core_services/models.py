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
    role_name = models.CharField(max_length=20, unique=True)
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
        return self.role_name


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


class Bank(models.Model):
    bank_code = models.CharField(max_length=255, unique=True)
    bank_name_th = models.CharField(max_length=255, null=True, blank=True)
    bank_name_eng = models.CharField(max_length=255, null=True, blank=True)

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
        return self.bank_code


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(
        Warehouse, null=True, blank=True, on_delete=models.SET_NULL
    )
    bank = models.ForeignKey(
        Bank, null=True, blank=True, on_delete=models.SET_NULL
    )
    id_card_number = models.TextField(null=True, blank=True)
    id_card_address = models.TextField(null=True, blank=True)
    current_address = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    bank_account = models.TextField(null=True, blank=True)
    car_license = models.TextField(null=True, blank=True)
    id_card_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="driver_info/",
        max_length=511,
    )
    driver_license = models.ImageField(
        null=True,
        blank=True,
        upload_to="driver_info/",
        max_length=511,
    )
    photo_with_card = models.ImageField(
        null=True,
        blank=True,
        upload_to="driver_info/",
        max_length=511,
    )
    profile_photo = models.ImageField(
        null=True,
        blank=True,
        upload_to="driver_info/",
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


class DriverJobRun(models.Model):
    # User who created the job run
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Date of the job run
    date = models.DateField()

    # Round of the job run
    round_info = models.CharField(max_length=30)

    # Remarks for the job run
    remarks = models.TextField(blank=True, null=True)
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
        return f"{self.date} - {self.round_info}"


class Mileage(models.Model):
    vehicle = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    mile = models.PositiveIntegerField()
    mile_image = models.ImageField(
        upload_to="mileage_images/", blank=True, null=True
    )
    front_image = models.ImageField(
        upload_to="vehicle_images/front/", blank=True, null=True
    )
    back_image = models.ImageField(
        upload_to="vehicle_images/back/", blank=True, null=True
    )
    left_image = models.ImageField(
        upload_to="vehicle_images/left/", blank=True, null=True
    )
    right_image = models.ImageField(
        upload_to="vehicle_images/right/", blank=True, null=True
    )
    update_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.update_date}"
