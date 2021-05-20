from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from expense.models import FixedCosts, FixedCostSourceCategory, FixedCostSource


class FixedCostView(LoginRequiredMixin, View):
    def get(self, request):
        fixed_costs = FixedCosts.objects.filter(user=request.user)
        paginator = Paginator(fixed_costs, 2)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'fixed/fixed_cost_view.html', {'pages': page, 'expenses': fixed_costs})

    def post(self, request):
        expense_id = request.POST['expense_id']
        FixedCosts.objects.get(pk=expense_id).delete()
        return redirect(reverse_lazy('income_panel'))


class AddFixedCostView(LoginRequiredMixin, View):
    def get(self, request):
        categories = FixedCostSourceCategory.objects.filter(user_id=request.user)
        sources = FixedCostSource.objects.all().prefetch_related('fixedcostsourcecategory_set')
        return render(request, 'fixed/add_fixed_cost_view.html', {'categories': categories, 'sources': sources})

    def post(self, request):
        amount = request.POST['fixed_amount']
        description = request.POST['fixed_description']
        date = request.POST['fixed_date']
        category_id = request.POST['category_id']
        category = FixedCostSourceCategory.objects.get(id=category_id)
        source_id = request.POST['source_id']
        source = FixedCostSource.objects.get(id=source_id)
        FixedCosts.objects.create(amount=amount, description=description, user=request.user, date=date,
                                  source=source, category=category)
        return redirect(reverse_lazy('expense_panel'))



class CreateCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'fixed/add_category_view.html')

    def post(self, request):
        category_name = request.POST['fixed_category']
        array = request.POST['categoriesString'].split(',')
        for elem in array:
            source = FixedCostSource.objects.create(name=elem, user=request.user)
        FixedCostSourceCategory.objects.create(name=category_name, user=request.user, sources=source)
        return redirect(reverse_lazy('expense_panel'))
