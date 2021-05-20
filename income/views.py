from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from income.models import Income, IncomeSource, IncomeSourceCategory


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


class CreateIncomeCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'income/add_category_view.html')

    def post(self, request):
        category_name = request.POST['income_category']
        array = request.POST['categoriesString'].split(',')
        for elem in array:
            IncomeSource.objects.create(name=elem, user=request.user)
        IncomeSourceCategory.objects.create(name=category_name, user=request.user)
        return redirect(reverse_lazy('income_panel'))


class AddIncomeView(LoginRequiredMixin, View):
    def get(self, request):
        all_categories = IncomeSourceCategory.objects.all()
        all_sources = IncomeSource.objects.all()
        return render(request, 'income/add_income_view.html', {'categories': all_categories, 'sources': all_sources})

    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        category = IncomeSourceCategory.objects.get(id=request.POST['category_id'])
        source = IncomeSource.objects.get(id=request.POST['source_id'])
        Income.objects.create(amount=amount, description=description, date=date,
                              category=category, source=source, user=request.user)
        return redirect(reverse_lazy('income_panel'))


class EditIncomeView(LoginRequiredMixin, View):
    def get(self, request, id):
        categories = IncomeSourceCategory.objects.filter(user_id=request.user)
        sources = IncomeSource.objects.all().prefetch_related('incomesourcecategory_set__sources')
        income_id = get_object_or_404(Income, pk=id)
        return render(request, 'income/edit_income_view.html', {'income': income_id, 'categories': categories,
                                                                'sources':sources})

    def post(self, request, id):
        get_income = get_object_or_404(Income, pk=id)
        get_source = IncomeSource.objects.get(pk=get_income.source_id)
        get_category = IncomeSourceCategory.objects.get(pk=get_income.category_id)
        get_category.name = request.POST['income_category']
        get_source.name = request.POST['income_source']
        get_income.amount = request.POST['income_amount']
        get_income.description = request.POST['income_description']
        get_income.date = request.POST['income_date']
        get_category.save()
        get_income.save()
        get_source.save()
        return redirect(reverse_lazy('income_panel'))
