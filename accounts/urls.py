from django.contrib import admin
from django.urls import path, include

from accounts import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),

]
