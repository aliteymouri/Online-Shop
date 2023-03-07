from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views import View
from .forms import *
from .mixins import *


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
                form.add_error('username', 'ایمیل یا گذرواژه وارد شده صحیح نمیباشد.')
        return render(req, self.template_name, {'form': form})


class SignUpView(AuthenticatedMixin, FormView):
    template_name = 'account/sign-up.html'
    form_class = SignUpForm
