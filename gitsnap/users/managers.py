from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name, password=None):
        """
        Creates and saves a User with the given email, 
        full_name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name, password=None):
        """
        Creates and saves a superuser with the given email, 
        full_name and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user