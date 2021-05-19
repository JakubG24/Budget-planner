from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from income.models import Income, IncomeSource


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class IncomeView(LoginRequiredMixin, View):
    def get(self, request):
        income = Income.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(income, 2)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'income/income_view.html', {'income_list': income, 'pages': page})

    def post(self, request):
        income_id = request.POST['income_id']
        income_to_del = Income.objects.get(pk=income_id)
        income_to_del.delete()
        return redirect(reverse_lazy('income_panel'))


class AddIncomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'income/add_income_view.html')

    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['income_source']
        income_source = IncomeSource.objects.create(name=source, user=request.user)
        income = Income.objects.create(amount=amount, description=description, date=date, source=income_source,
                                       user=request.user)
        income.save()
        return redirect(reverse_lazy('income_panel'))


class EditIncomeView(LoginRequiredMixin, View):
    def get(self, request, id):
        income_id = get_object_or_404(Income, pk=id)
        return render(request, 'income/edit_income_view.html', {'income': income_id})

    def post(self, request, id):
        get_income = get_object_or_404(Income, pk=id)
        get_source = IncomeSource.objects.get(pk=get_income.source_id)
        get_source.name = request.POST['income_source']
        get_income.amount = request.POST['amount']
        get_income.description = request.POST['description']
        get_income.date = request.POST['income_date']
        get_income.save()
        get_source.save()
        return redirect(reverse_lazy('income_panel'))
