from django.db import models
from django.utils import timezone

from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    email = models.EmailField("پست الکترونیک", unique=True)
    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True, )
    fullname = models.CharField('نام و نام خوانوادگی', max_length=100, null=True, blank=True)
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
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField('توکن اعتبارسنجی', max_length=155, null=True)
    phone_number = models.CharField('شماره موبایل', max_length=11)
    code = models.CharField(' کد فعالسازی', max_length=5)
    expiration = models.DateTimeField('تاریخ انقضا', null=True, blank=True)

    def __str__(self):
        return F" : شماره موبایل  {self.phone_number}"

    def is_not_expired(self):
        if self.expiration >= timezone.localtime(timezone.now()):
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "کدهای اعتبارسنجی"
        verbose_name = "کد اعتبارسنجی"
