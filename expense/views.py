from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from expense.forms import FixedCostForm
from expense.models import FixedCosts, FixedCostSourceCategory, FixedCostSource, VariableCosts


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


# class AddFixedCostView(LoginRequiredMixin, View):
#     def get(self, request):
#         categories = FixedCostSourceCategory.objects.filter(user_id=request.user)
#         sources = FixedCostSource.objects.all().prefetch_related('fixedcostsourcecategory_set')
#         return render(request, 'fixed/add_fixed_cost_view.html', {'categories': categories, 'sources': sources})
#
#     def post(self, request):
#         amount = request.POST['fixed_amount']
#         description = request.POST['fixed_description']
#         date = request.POST['fixed_date']
#         category_id = request.POST['category_id']
#         category = FixedCostSourceCategory.objects.get(id=category_id)
#         source_id = request.POST['source_id']
#         source = FixedCostSource.objects.get(id=source_id)
#         FixedCosts.objects.create(amount=amount, description=description, user=request.user, date=date,
#                                   source=source, category=category)
#         return redirect(reverse_lazy('fixed_cost_view'))


class AddFixedCostView(LoginRequiredMixin, CreateView):
    model = FixedCosts
    form_class = FixedCostForm
    template_name = 'fixed/add_fixed_cost_view.html'
    success_url = reverse_lazy('fixed_cost_view')


def load_sources(request):
    category_id = request.GET.get('category')
    sources = FixedCostSource.objects.filter(source_id=category_id)
    return render(request, 'source_dropdown_list_option.html', {'sources': sources})


class EditFixedCostView(LoginRequiredMixin, View):
    def get(self, request, id):
        categories = FixedCostSourceCategory.objects.filter(user_id=request.user)
        sources = FixedCostSource.objects.all().prefetch_related('fixedcostsourcecategory_set')
        expense_id = get_object_or_404(FixedCosts, pk=id)
        return render(request, 'fixed/edit_fixed_view.html', {'expense': expense_id, 'categories': categories,
                                                              'sources': sources})

    def post(self, request, id):
        get_expense = get_object_or_404(FixedCosts, pk=id)
        get_source = FixedCostSource.objects.get(pk=get_expense.source_id)
        get_category = FixedCostSourceCategory.objects.get(pk=get_expense.category_id)
        get_category.name = request.POST['expense_category']
        get_source.name = request.POST['expense_source']
        get_expense.amount = request.POST['expense_amount']
        get_expense.description = request.POST['expense_description']
        get_expense.date = request.POST['expense_date']
        get_category.save()
        get_expense.save()
        get_source.save()
        return redirect(reverse_lazy('fixed_cost_view'))


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
