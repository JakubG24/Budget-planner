from django.urls import path, include

from expense import views

urlpatterns = [
    path('', views.ExpensePanelView.as_view(), name='expense_panel'),
    path('fixed_costs/', views.FixedCostView.as_view(), name='fixed_cost_view'),
    path('fixed_cost_category/<int:id>/add_source/', views.AddFixedSourceView.as_view(), name='fixed_add_source'),
    path('variable_cost_category/<int:id>/add_source/', views.AddVariableSourceView.as_view(), name='variable_add_source'),
    path('fixed_cost_category/edit/<int:id>/', views.FixedCostCategoryEdit.as_view(), name='fixed_category_edit'),
    path('variable_cost_category/edit/<int:id>/', views.VariableCostCategoryEdit.as_view(),
         name='variable_category_edit'),
    path('fixed_cost_source/edit/<int:id>/', views.FixedCostSourceEdit.as_view(), name='fixed_source_edit'),
    path('variable_cost_source/edit/<int:id>/', views.VariableCostSourceEdit.as_view(), name='variable_source_edit'),
    path('fixed_cost_category/<int:id>/', views.FixedCostCategoryDetails.as_view(), name='fixed_category_details'),
    path('variable_cost_category/<int:id>/', views.VariableCostCategoryDetails.as_view(),
         name='variable_category_details'),
    path('add_expense/fixed/', views.AddFixedCostView.as_view(), name='add_fixed'),
    path('add_expense/variable/', views.VariableCostAddView.as_view(), name='add_variable'),
    path('create_category/fixed/', views.CreateCategoryView.as_view(), name='create_category_fixed'),
    path('create_category/variable/', views.CreateCategoryVariableView.as_view(), name='create_category_variable'),
    path('fixed_costs/edit/<int:pk>/', views.EditFixedCostView.as_view(), name='edit_fixed'),
    path('variable_costs/edit/<int:pk>/', views.EditVariableCostView.as_view(), name='edit_variable'),
    path('variable_costs/', views.VariableCostView.as_view(), name='variable_cost_view'),
    path('load-sources/fixed/', views.load_sources, name='load_sources_fixed'),
    path('load-sources/variable/', views.load_sources_variable, name='load_sources_variable'),
    path('summary/comparative_chart/', views.ExpenseComparisonChartView.as_view(), name='comparative_chart'),
    path('summary/fixed_costs/chart/', views.FixedCostsChartView.as_view(), name='fixed_cost_chart'),
    path('summary/variable_costs/chart/', views.VariableCostsChartView.as_view(), name='variable_cost_chart'),
]
