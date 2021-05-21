from django.contrib import admin

from expense.models import FixedCosts, FixedCostSource, FixedCostSourceCategory, VariableCosts, VariableCostSource, \
    VariableCostSourceCategory

admin.site.register(FixedCosts)
admin.site.register(FixedCostSource)
admin.site.register(FixedCostSourceCategory)
admin.site.register(VariableCosts)
admin.site.register(VariableCostSource)
admin.site.register(VariableCostSourceCategory)
