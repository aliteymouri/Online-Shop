from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, password=None):

        if not phone_number:
            raise ValueError(_('Users must have a phone_number'))

        if not email:
            raise ValueError(_('Users must have an email'))

        user = self.model(
            phone_number=phone_number,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None):
        """
        Creates and saves a superuser with the given email phone and password.
        """
        user = self.create_user(
            password=password,
            phone_number=phone_number,
            email=email
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
