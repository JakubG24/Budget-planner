from django.contrib import admin

# Register your models here.
from income.models import Income, IncomeSource, IncomeSourceCategory

admin.site.register(Income)
admin.site.register(IncomeSource)
admin.site.register(IncomeSourceCategory)
