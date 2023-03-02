from django.db import models
from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name=_('username'),
        max_length=40,
        unique=True, )
    email = models.EmailField("پست الکترونیک", unique=True)
    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True, )
    melli_code = models.CharField("کد ملی", max_length=10, blank=True)
    avatar = models.FileField(upload_to="users/profile", null=True,
                              blank=True, verbose_name='عکس پروفایل')

    is_active = models.BooleanField('وضعیت کاربر', default=True)
    is_admin = models.BooleanField('مدیر', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
