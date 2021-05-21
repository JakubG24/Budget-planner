from django.urls import path, include

from expense import views

urlpatterns = [
    path('', views.ExpensePanelView.as_view(), name='expense_panel'),
    path('fixed_costs/', views.FixedCostView.as_view(), name='fixed_cost_view'),
    path('add_expense/fixed/', views.AddFixedCostView.as_view(), name='add_fixed'),
    path('create_category/fixed/', views.CreateCategoryView.as_view(), name='create_category_fixed'),
    path('fixed_costs/edit/<int:id>/', views.EditFixedCostView.as_view(), name='edit_fixed'),
    path('variable_costs/', views.VariableCostView.as_view(), name='variable_cost_view'),
    path('ajax/load-sources/', views.load_sources, name='ajax_load_sources'),

]
