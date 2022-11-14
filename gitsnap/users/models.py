from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from gitsnap.common.models import BaseModel
from gitsnap.users.managers import UserManager


class User(BaseModel, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(blank=True)
    full_name = models.CharField(verbose_name="full name", max_length=200)
    avatar = models.ImageField(upload_to='avatars')
    bio = models.TextField(blank=True, null=True)

    password_reset_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(verbose_name="date joined", default=timezone.now)
    last_login_ip = models.GenericIPAddressField(verbose_name="last login ip", blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

