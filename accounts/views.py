from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/login.html'


class AccountSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'registration/account_details.html')

    def post(self, request):
        return redirect(reverse_lazy('change_password'))


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'registration/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            success_message = 'Your password has been changed successfully!'
            return render(request, 'registration/account_details.html', {'msg': success_message})
        return render(request, 'registration/change_password.html', {'form': form})


