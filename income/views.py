from datetime import datetime, date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView

from income.forms import IncomeForm
from income.models import Income, IncomeSource, IncomeSourceCategory


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class IncomeView(LoginRequiredMixin, View):
    def get(self, request):
        income = Income.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(income, 12)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'income/income_view.html', {'income_list': income, 'pages': page})

    def post(self, request):
        income_id = request.POST['income_id']
        income_to_del = Income.objects.get(pk=income_id)
        income_to_del.delete()
        return redirect(reverse_lazy('income_panel'))


class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'income/add_category_view.html')

    def post(self, request):
        category_name = request.POST.get('income_category')
        array = request.POST['categoriesString'].split(',')
        category = IncomeSourceCategory.objects.create(name=category_name, user=request.user)
        for elem in array:
            ic = IncomeSource.objects.create(name=elem, user=request.user)
        ic.sources.add(category)
        return redirect(reverse_lazy('income_panel'))


class AddIncomeView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('income_panel')
    template_name = 'income/add_income_view.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddIncomeView, self).form_valid(form)


class EditIncomeView(LoginRequiredMixin, UpdateView):
    model = Income
    template_name = 'income/edit_income_view.html'
    success_url = reverse_lazy('income_panel')
    fields = ('amount', 'date', 'description', 'category', 'source')


class IncomeChartView(View):
    def get(self, request):
        labels = []
        data = []
        queryset = Income.objects.filter(user=request.user).annotate(month=TruncMonth('date')).values('month').\
            annotate(s=Sum('amount')).values('month', 's')
        for income in queryset:
            labels.append(income['month'])
            data.append(income['s'])
        total_amount = f'Total income: {round(sum(data), 2)}'
        return render(request, 'income/charts/current_year_chart.html', {'labels': labels, 'data': data,
                                                                         'total': total_amount})

    def post(self, request):
        to_date = request.POST['to_date']
        from_date = request.POST['from_date']
        labels = []
        data = []
        queryset = Income.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date)\
            .values('category__name').annotate(category_amount=Sum('amount')).order_by('-category_amount')
        for income in queryset:
            labels.append(income['category__name'])
            data.append(income['category_amount'])
        return render(request, 'income/charts/date_filter_chart.html', {'labels': labels, 'data': data})

