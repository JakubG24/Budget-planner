from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from expense.models import FixedCosts


class FixedCostView(LoginRequiredMixin, View):
    def get(self, request):
        fixed_costs = FixedCosts.objects.filter(user=request.user)
        paginator = Paginator(fixed_costs, 2)
        page_number = request.GET.get('page')
        page = Paginator.get_page(paginator, page_number)
        return render(request, 'fixed/fixed_cost_view.html', {'pages': page, 'expenses': fixed_costs})


class AddFixedCostView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'fixed/add_fixed_cost_view.html')
