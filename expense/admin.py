from django.contrib import admin

from expense.models import FixedCosts, FixedCostSource

admin.site.register(FixedCosts)
admin.site.register(FixedCostSource)
