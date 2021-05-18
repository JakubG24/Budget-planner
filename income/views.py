from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from income.models import Income


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class IncomeView(LoginRequiredMixin, View):
    def get(self, request):
        income = Income.objects.filter(user=request.user).order_by('date')
        paginator = Paginator(income, 1)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'income/income_view.html', {'income_list': income, 'pages': page})


class AddIncomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'income/add_income_view.html')

    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        income = Income.objects.create(amount=amount, description=description, date=date, user=request.user)
        income.save()
        return redirect(reverse_lazy('income_panel'))
