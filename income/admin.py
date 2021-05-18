from django.contrib import admin

# Register your models here.
from income.models import Income, IncomeSource

admin.site.register(Income)
admin.site.register(IncomeSource)
