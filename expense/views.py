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
        fixed_costs = FixedCosts.objects.filter(user=request.user)
        paginator = Paginator(fixed_costs, 5)
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
        paginator = Paginator(variable_costs, 5)
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


class ExpenseComparisonChartView(View):
    def get(self, request):
        labels = []
        data = []
        labels2 = []
        data2 = []
        queryset2 = VariableCosts.objects.filter(user=request.user).annotate(month=ExtractMonth('date')).values('month'). \
            annotate(s=Sum('amount')).values('month', 's').order_by('month')
        for expense in queryset2:
            labels.append(calendar.month_name[expense['month']])
            data2.append(expense['s'])
        total_amount2 = round(sum(data2), 2)
        queryset = FixedCosts.objects.filter(user=request.user).annotate(month=ExtractMonth('date')).values('month'). \
            annotate(s=Sum('amount')).values('month', 's').order_by('month')
        for expense in queryset:
            labels.append(calendar.month_name[expense['month']])
            data.append(expense['s'])
        total_amount = round(sum(data), 2)
        return render(request, 'charts/expense_comparison_chart.html', {'labels': labels, 'data': data,
                                                                        'total': total_amount+total_amount2, 'labels2': labels2,
                                                                        'data2': data2})


