"""BudgetPlanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from income import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/', include('accounts.urls')),
    path('expense/', include('expense.urls')),
    path('income/my_income/', views.IncomeView.as_view(), name='income_panel'),
    path('income/my_income/add_income/', views.AddIncomeView.as_view(), name='add_income'),
    path('income/my_income/edit/<int:pk>/', views.EditIncomeView.as_view(), name='edit_income'),
    path('income/create_category/', views.CreateCategoryView.as_view(), name='income_category'),
    path('summary/income_charts/', views.IncomeChartView.as_view(), name='income_charts'),
    path('summary/total/', views.TotalSummaryView.as_view(), name='total_summary_chart'),
]
