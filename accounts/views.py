from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import *

from .forms import *
from .mixins import *
from uuid import uuid4
from .models import Otp
from random import randint
from accounts import messages


class SignInView(AuthenticatedMixin, FormView):
    template_name = 'account/sign-in.html'
    form_class = SignInForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(req.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(req, user)
                return redirect('home:home')
            else:
                form.add_error('username', messages.WRONG_PASSWORD_OR_EMAIL)
        return render(req, self.template_name, {'form': form})


class SignUpView(AuthenticatedMixin, CreateView):
    template_name = 'account/sign-up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = uuid4().hex
        code = randint(10000, 99999)
        expiration = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=15)
        Otp.objects.create(token=token, code=code, expiration=expiration,
                           phone_number=form.cleaned_data.get('phone_number'))
        print(code)

        # SMS.verification(
        #     {'receptor': form.cleaned_data["phone_number"], 'type': '1', 'templates': 'randecode', 'param1': code}
        # )

        return redirect(reverse_lazy('accounts:check-otp') + f'?token={token}')


class CheckOtpView(FormView):
    template_name = 'account/check-otp.html'
    form_class = CheckOtpForm

    def form_valid(self, form):
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        if otp.is_not_expired():
            if form.cleaned_data['code'] == otp.code:
                user = User.objects.get(phone_number=otp.phone_number)
                user.is_active = True
                user.save()
                login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return render(self.request, 'account/welcome.html')
            form.add_error('code', messages.WRONG_OTP_CODE)
            return render(self.request, self.template_name, {"form": form})
        otp.delete()
        User.objects.get(phone_number=otp.phone_number).delete()
        form.add_error('code', messages.EXPIRED_OTP)
        return render(self.request, self.template_name, {"form": form})

    def get_context_data(self, **kwargs):
        context = super(CheckOtpView, self).get_context_data(**kwargs)
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        context["user"] = User.objects.get(phone_number=otp.phone_number)
        return context


class PersonalInfoView(View):
    template_name = 'account/personal_info.html'

    def get(self, req):
        return render(req, self.template_name, {'instance': req.user})


class EditPersonalInfoView(TemplateView):
    template_name = 'account/edit-personal-info.html'
