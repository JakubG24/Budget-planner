import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from income.models import Income


@pytest.mark.django_db
def test_get_user(user):
    obj = User.objects.all()
    assert obj.count() == 1


@pytest.mark.django_db
def test_index_view_get():
    c = Client()
    response = c.get(reverse('index'))
    assert response.status_code == 200


'''INCOME TESTS'''
@pytest.mark.django_db
def test_add_income_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('add_income'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_income_get_logged_in(user):
    c = Client()
    c.force_login(user)

    response = c.get(reverse('add_income'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_income_post(category_source):
    c = Client()
    c.force_login(category_source.user)
    incomes_before = Income.objects.count()
    response = c.post(reverse('add_income'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                              'category': category_source.categories.first().id,
                                              'source': [category_source.id]})
    assert response.status_code == 302
    assert Income.objects.count() == incomes_before + 1


@pytest.mark.django_db
def test_modify_income(category_source):
    c = Client()
    c.force_login(category_source.user)
    c.post(reverse('add_income'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                   'category': category_source.categories.first().id,
                                   'source': [category_source.id]})
    income = Income.objects.first()
    assert income.amount == 500.0
    response = c.get(reverse('edit_income', kwargs={'pk': income.id}))
    assert response.status_code == 200
    Income.objects.filter(id=income.id).update(amount=600)
    income.refresh_from_db()
    assert income.amount == 600


@pytest.mark.django_db
def test_delete_income(category_source):
    c = Client()
    c.force_login(category_source.user)
    c.post(reverse('add_income'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                   'category': category_source.categories.first().id,
                                   'source': [category_source.id]})

    assert Income.objects.count() == 1
    income = Income.objects.first()
    income.delete()
    assert Income.objects.count() == 0


'''INCOME SUMMARY TESTS'''
@pytest.mark.django_db
def test_income_summary_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('income_charts'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_income_summary_post(user):
    c = Client()
    c.force_login(user)
    response = c.post(reverse('income_charts'), {'from_date': '2021-05-01', 'to_date': '2021-05-30'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_total_summary_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('total_summary_chart'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
