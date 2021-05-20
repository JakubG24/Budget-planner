from django.urls import path, include

from expense import views

urlpatterns = [
    path('fixed_costs/', views.FixedCostView.as_view(), name='expense_panel'),
    path('add_expense/fixed/', views.AddFixedCostView.as_view(), name='add_fixed'),
    path('create_category/fixed/', views.CreateCategoryView.as_view(), name='create_category_fixed'),


]
