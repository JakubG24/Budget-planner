from datetime import datetime
from itertools import chain
from operator import attrgetter
from xxlimited import Null

import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from expense.forms import FixedCostForm, VariableCostForm
from expense.models import FixedCosts, FixedCostSourceCategory, FixedCostSource, VariableCosts, VariableCostSource, \
    VariableCostSourceCategory


class FixedCostView(LoginRequiredMixin, View):
    def get(self, request):
        fixed_costs = FixedCosts.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(fixed_costs, 12)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'fixed/fixed_cost_view.html', {'pages': page, 'expenses': fixed_costs})

    def post(self, request):
        expense_id = request.POST['expense_id']
        FixedCosts.objects.get(pk=expense_id).delete()
        return redirect(reverse_lazy('fixed_cost_view'))


class AddFixedCostView(LoginRequiredMixin, CreateView):
    model = FixedCosts
    form_class = FixedCostForm
    success_url = reverse_lazy('fixed_cost_view')
    template_name = 'fixed/add_fixed_cost_view.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddFixedCostView, self).form_valid(form)


def load_sources(request):
    category_id = request.GET.get('category')
    sources = FixedCostSource.objects.filter(source_id=category_id)
    return render(request, 'source_dropdown_list_option.html', {'sources': sources})


class EditFixedCostView(LoginRequiredMixin, UpdateView):
    model = FixedCosts
    template_name = 'fixed/edit_fixed_view.html'
    success_url = reverse_lazy('fixed_cost_view')
    fields = ('amount', 'date', 'description', 'category', 'source')


class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_category_view.html')

    def post(self, request):
        category_name = request.POST['fixed_category']
        array = request.POST['categoriesString'].split(',')
        category = FixedCostSourceCategory.objects.create(name=category_name, user=request.user)
        for elem in array:
            FixedCostSource.objects.create(name=elem, user=request.user, source=category)
        return redirect(reverse_lazy('fixed_cost_view'))


class ExpensePanelView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'expense_panel.html')


class VariableCostView(LoginRequiredMixin, View):
    def get(self, request):
        variable_costs = VariableCosts.objects.filter(user=request.user)
        paginator = Paginator(variable_costs, 12)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'variable/variable_cost_view.html', {'pages': page, 'expenses': variable_costs})

    def post(self, request):
        expense_id = request.POST['expense_id']
        VariableCosts.objects.get(pk=expense_id).delete()
        return redirect(reverse_lazy('variable_cost_view'))


class VariableCostAddView(LoginRequiredMixin, CreateView):
    model = VariableCosts
    form_class = VariableCostForm
    success_url = reverse_lazy('variable_cost_view')
    template_name = 'variable/add_variable_cost_view.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VariableCostAddView, self).form_valid(form)


def load_sources_variable(request):
    category_id = request.GET.get('category')
    sources = VariableCostSource.objects.filter(source_id=category_id)
    return render(request, 'source_dropdown_list_option.html', {'sources': sources})


class CreateCategoryVariableView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_category_view.html')

    def post(self, request):
        category_name = request.POST['fixed_category']
        array = request.POST['categoriesString'].split(',')
        category = VariableCostSourceCategory.objects.create(name=category_name, user=request.user)
        for elem in array:
            VariableCostSource.objects.create(name=elem, user=request.user, source=category)
        return redirect(reverse_lazy('variable_cost_view'))


class EditVariableCostView(LoginRequiredMixin, UpdateView):
    model = VariableCosts
    template_name = 'variable/edit_variable_cost_view.html'
    success_url = reverse_lazy('variable_cost_view')
    fields = ('amount', 'date', 'description', 'category', 'source')


class ExpenseComparisonChartView(LoginRequiredMixin, View):
    def get(self, request):
        labels = []
        for x in range(1, 13):
            labels.append(calendar.month_name[x])
        data = []
        data2 = []
        for month in range(1, 13):
            queryset = FixedCosts.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset:
                data.append(0.0)
            else:
                data.append(queryset[0]['s'])

            queryset2 = VariableCosts.objects.filter(user=request.user, date__month=month).values('date__month'). \
                annotate(s=Sum('amount')).order_by('date__month')
            if not queryset2:
                data2.append(0.0)
            else:
                data2.append(queryset2[0]['s'])
        total = round(sum(data) + sum(data2), 2)
        return render(request, 'charts/expense_comparative_chart.html', {'total': total, 'labels': labels, 'data': data,
                                                                        'data2': data2})


class FixedCostsChartView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'charts/fixed_cost_chart.html')

    def post(self, request):
        to_date = request.POST['to_date']
        from_date = request.POST['from_date']
        labels = []
        data = []
        queryset = FixedCosts.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(category_amount=Sum('amount')).order_by('-category_amount')
        for expense in queryset:
            labels.append(expense['category__name'])
            data.append(expense['category_amount'])
        return render(request, 'charts/fixed_cost_chart.html', {'labels': labels, 'data': data})


class VariableCostsChartView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'charts/variable_cost_chart.html')

    def post(self, request):
        to_date = request.POST['to_date']
        from_date = request.POST['from_date']
        labels = []
        data = []
        queryset = VariableCosts.objects.filter(user=request.user, date__gte=from_date, date__lte=to_date) \
            .values('category__name').annotate(category_amount=Sum('amount')).order_by('-category_amount')
        for expense in queryset:
            labels.append(expense['category__name'])
            data.append(expense['category_amount'])
        return render(request, 'charts/variable_cost_chart.html', {'labels': labels, 'data': data})
