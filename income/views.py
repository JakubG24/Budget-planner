from django.shortcuts import render
from django.views import View

from income.models import Income


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class IncomeView(View):
    def get(self, request):
        incomes = Income.objects.all()
        return render(request, 'income/income_view.html', {'incomes': incomes})
