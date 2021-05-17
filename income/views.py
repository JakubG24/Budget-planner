from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from income.models import Income


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class IncomeView(View):
    def get(self, request):
        income = Income.objects.filter(user=request.user).order_by('date')
        paginator = Paginator(income, 1)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'income/income_view.html', {'income_list': income, 'pages': page})
