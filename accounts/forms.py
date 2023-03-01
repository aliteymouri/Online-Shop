from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه مشابه نمیباشد")
        elif len(password1 and password2) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise ValidationError("نام کاربری باید شامل حداقل ۴ کاراکتر باشد")
        return username

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number',
                  'melli_code', 'avatar', 'is_active', 'is_admin')
