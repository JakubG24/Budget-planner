from django.contrib import admin

from expense.models import FixedCosts, FixedCostSource, FixedCostSourceCategory

admin.site.register(FixedCosts)
admin.site.register(FixedCostSource)
admin.site.register(FixedCostSourceCategory)
