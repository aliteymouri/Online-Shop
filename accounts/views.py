from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views import View
from .forms import *


class SignInView(FormView):
    template_name = 'account/sign-in.html'
    form_class = SignInForm

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(self.request, user)
                return redirect('home:home')
            else:
                form.add_error('username', 'ایمیل یا گذرواژه وارد شده صحیح نمیباشد.')
        return render(self.request, self.template_name, {'form': form})
