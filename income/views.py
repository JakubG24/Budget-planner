import calendar
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView

from expense.models import FixedCosts, VariableCosts
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


class IncomeChartView(LoginRequiredMixin, View):
    def get(self, request):
        labels = []
        for x in range(1, 13):
            labels.append(calendar.month_name[x])
        data = []
        for month in range(1, 13):
            queryset = Income.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset:
                data.append(0.0)
            else:
                data.append(queryset[0]['s'])
        total_amount = f'Total income: {round(sum(data), 2)}'
        request.session['total_income'] = data
        return render(request, 'income/charts/current_year_chart.html', {'labels': labels, 'data': data,
                                                                         'total': total_amount})

    def post(self, request):
        to_date = request.POST['to_date']
        from_date = request.POST['from_date']
        labels = []
        data = []
        queryset = Income.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(category_amount=Sum('amount')).order_by('-category_amount')
        for income in queryset:
            labels.append(income['category__name'])
            data.append(income['category_amount'])
        return render(request, 'income/charts/date_filter_chart.html', {'labels': labels, 'data': data})


class TotalSummaryView(LoginRequiredMixin, View):
    def get(self, request):
        income_data = []
        data2 = []
        data3 = []
        labels = []
        for x in range(1, 13):
            labels.append(calendar.month_name[x])

        for month in range(1, 13):
            queryset = Income.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset:
                income_data.append(0.0)
            else:
                income_data.append(queryset[0]['s'])

            queryset1 = FixedCosts.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset1:
                data2.append(0.0)
            else:
                data2.append(queryset1[0]['s'])

            queryset2 = VariableCosts.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset2:
                data3.append(0.0)
            else:
                data3.append(queryset2[0]['s'])
        expense_data = [x + y for (x, y) in zip(data2, data3)]
        current_year = datetime.now().year
        income_sum = round(sum(income_data), 2)
        expense_sum = round(sum(expense_data), 2)
        return render(request, 'total_summary_chart.html', {'labels': labels, 'income': income_data,
                                                            'expense': expense_data, 'year': current_year,
                                                            'total_inc': income_sum, 'total_exp': expense_sum})

    def post(self, request):
        income_data = []
        data1 = []
        data2 = []
        to_date = request.POST['to_date']
        from_date = request.POST['from_date']
        queryset = Income.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(s=Sum('amount'))
        income_data.append(queryset[0]['s'])

        queryset1 = FixedCosts.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(s=Sum('amount'))
        data1.append(queryset1[0]['s'])

        queryset2 = VariableCosts.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(s=Sum('amount'))
        data2.append(queryset2[0]['s'])

        expense_data = [x + y for (x, y) in zip(data1, data2)]
        income_sum = round(sum(income_data), 2)
        expense_sum = round(sum(expense_data), 2)
        return render(request, 'summary_pie_chart.html', {'income': income_data, 'expense': expense_data,
                                                          'total_inc': income_sum, 'total_exp': expense_sum})
