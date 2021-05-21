from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
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
        paginator = Paginator(income, 5)
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
