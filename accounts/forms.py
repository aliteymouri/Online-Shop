from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User


def check_number(value):
    if value[:2] != "09" or len(value) < 11:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')
    try:
        int(value)
    except:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)
    phone_number = forms.CharField(widget=forms.TextInput({'placeholder': 'شماره موبایل', 'maxlength': 11}),
                                   validators=[check_number])

    class Meta:
        model = User
        fields = ('phone_number', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه مشابه نمیباشد")
        elif len(password1 and password2) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    phone_number = forms.CharField(widget=forms.TextInput({'placeholder': 'شماره موبایل', 'maxlength': 11}),
                                   validators=[check_number])

    class Meta:
        model = User
        fields = ('password', 'email', 'phone_number',
                  'melli_code', 'avatar', 'is_active', 'is_admin')


class SignInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': 'پست الکترونیک یا شماره موبایل خود را وارد نمایید'}))

    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'input-field', 'placeholder': 'رمز عبور خود را وارد نمایید'}))


class SignUpForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' شماره موبایل خود را وارد نمایید ', 'maxlength': 11}),
        validators=[check_number])
    email = forms.EmailField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' پست الکترونیک خود را وارد نمایید '}))
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'input-field', 'placeholder': ' رمز عبور خود را وارد نمایید '}))

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password']


class CheckOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' کد تایید را وارد نمایید ', 'maxlength': 5}))


class EditPersonalInfoForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    fullname = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': 'نام و نام خوانوادگی خود را وارد نمایید '}))
    melli_code = forms.IntegerField(required=False,
                                    widget=forms.TextInput(
                                        {'class': 'input-field', 'placeholder': ' کد ملی خود را وارد کنید '}))
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' شماره موبایل خود را وارد نمایید ', 'maxlength': 11}),
        validators=[check_number])
    email = forms.EmailField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' پست الکترونیک خود را وارد نمایید '}))
    card_number = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      {'class': 'input-field', 'placeholder': 'شماره کارت خود را وارد نمایید '}))

    class Meta:
        model = User
        fields = ['avatar', 'fullname', 'melli_code',
                  'phone_number', 'email', 'card_number']


class ChangePassForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': 'رمز عبور قبلی خود را وارد نمایید '}))

    new_password = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': 'رمز عبور جدید خود را وارد نمایید '}))

    repeat_new_password = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': 'رمز عبور جدید خود را مجدد وارد نمایید '}))
