import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from expense.models import FixedCosts, VariableCosts, FixedCostSourceCategory, FixedCostSource, \
    VariableCostSourceCategory, VariableCostSource


@pytest.mark.django_db
def test_get_user(user):
    obj = User.objects.all()
    assert obj.count() == 1


'''////////////////EXPENSE PANEL TESTS////////////////'''


@pytest.mark.django_db
def test_expense_panel_not_logged_in():
    c = Client()
    response = c.get(reverse('expense_panel'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_expense_panel_logged_in(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('expense_panel'))
    assert response.status_code == 200


'''////////////////FIXED COST TESTS////////////////'''


@pytest.mark.django_db
def test_add_fixed_cost_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('add_fixed'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_fixed_cost_get_logged_in(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('add_fixed'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_fixed_cost_post(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category_source.user)
    fixed_costs_before = FixedCosts.objects.count()
    response = c.post(reverse('add_fixed'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                             'category': fixed_cost_category.id,
                                             'source': fixed_cost_category_source.id})
    assert response.status_code == 302
    assert FixedCosts.objects.count() == fixed_costs_before + 1


@pytest.mark.django_db
def test_modify_fixed_cost(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category_source.user)
    c.post(reverse('add_fixed'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                  'category': fixed_cost_category.id,
                                  'source': fixed_cost_category_source.id})
    fixed_cost = FixedCosts.objects.first()
    assert fixed_cost.amount == 500.0
    response = c.get(reverse('edit_fixed', kwargs={'pk': fixed_cost.id}))
    assert response.status_code == 200
    FixedCosts.objects.filter(id=fixed_cost.id).update(amount=600)
    fixed_cost.refresh_from_db()
    assert fixed_cost.amount == 600


@pytest.mark.django_db
def test_delete_fixed_cost(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category_source.user)
    c.post(reverse('add_fixed'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                  'category': fixed_cost_category.id,
                                  'source': fixed_cost_category_source.id})
    assert FixedCosts.objects.count() == 1
    fixed_cost = FixedCosts.objects.first()
    fixed_cost.delete()
    assert FixedCosts.objects.count() == 0


'''////////////////FIXED COST CHARTS TESTS////////////////'''


@pytest.mark.django_db
def test_expense_comparison_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('comparative_chart'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_fixed_cost_chart_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('fixed_cost_chart'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_fixed_cost_chart_post(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('fixed_cost_chart'), {'from_date': '2021-05-01', 'to_date': '2021-05-30'})
    assert response.status_code == 200


'''////////////////VARIABLE COST TESTS////////////////'''


@pytest.mark.django_db
def test_add_variable_cost_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('add_variable'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_variable_cost_get_logged_in(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('add_variable'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_variable_cost_post(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category_source.user)
    variable_costs_before = VariableCosts.objects.count()
    response = c.post(reverse('add_variable'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                                'category': variable_cost_category.id,
                                                'source': variable_cost_category_source.id})
    assert response.status_code == 302
    assert VariableCosts.objects.count() == variable_costs_before + 1


@pytest.mark.django_db
def test_modify_variable_cost(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category_source.user)
    c.post(reverse('add_variable'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                     'category': variable_cost_category.id,
                                     'source': variable_cost_category_source.id})
    variable_cost = VariableCosts.objects.first()
    assert variable_cost.amount == 500.0
    response = c.get(reverse('edit_variable', kwargs={'pk': variable_cost.id}))
    assert response.status_code == 200
    VariableCosts.objects.filter(id=variable_cost.id).update(amount=600)
    variable_cost.refresh_from_db()
    assert variable_cost.amount == 600


@pytest.mark.django_db
def test_delete_variable_cost(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category_source.user)
    c.post(reverse('add_variable'), {'amount': 500, 'date': '2021-05-05', 'description': 'test',
                                     'category': variable_cost_category.id,
                                     'source': variable_cost_category_source.id})
    assert VariableCosts.objects.count() == 1
    variable_cost = VariableCosts.objects.first()
    variable_cost.delete()
    assert VariableCosts.objects.count() == 0


'''////////////////VARIABLE COST CHARTS TESTS////////////////'''


@pytest.mark.django_db
def test_variable_cost_chart_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('variable_cost_chart'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_fixed_cost_chart_post(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('variable_cost_chart'), {'from_date': '2021-05-01', 'to_date': '2021-05-30'})
    assert response.status_code == 200


'''////////////////FIXED COST CATEGORIES TESTS////////////////'''


@pytest.mark.django_db
def test_category_details_get(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    response = c.get(reverse('fixed_category_details', kwargs={'id': fixed_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_edit_get(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    response = c.get(reverse('fixed_category_edit', kwargs={'id': fixed_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_edit_post(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    assert fixed_cost_category.name == 'blee'
    response = c.post(reverse('fixed_category_edit', kwargs={'id': fixed_cost_category.id}), {'name': 'test'})
    fixed_cost_category.refresh_from_db()
    assert fixed_cost_category.name == 'test'
    assert response.status_code == 302


@pytest.mark.django_db
def test_category_delete(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    assert FixedCostSourceCategory.objects.count() == 1
    fixed_cost_category.delete()
    assert FixedCostSourceCategory.objects.count() == 0


@pytest.mark.django_db
def test_source_add_get(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    response = c.get(reverse('fixed_add_source', kwargs={'id': fixed_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_source_add_post(fixed_cost_category):
    c = Client()
    c.force_login(fixed_cost_category.user)
    assert FixedCostSource.objects.count() == 0
    response = c.post(reverse('fixed_add_source', kwargs={'id': fixed_cost_category.id}), {'name': 'test'})
    assert response.status_code == 302
    assert FixedCostSource.objects.count() == 1


@pytest.mark.django_db
def test_category_source_edit_get(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category.user)
    response = c.get(reverse('fixed_source_edit', kwargs={'id': fixed_cost_category_source.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_source_edit_post(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category.user)
    assert fixed_cost_category_source.name == 'bleeh'
    response = c.post(reverse('fixed_source_edit', kwargs={'id': fixed_cost_category_source.id}), {'name': 'test'})
    fixed_cost_category_source.refresh_from_db()
    assert fixed_cost_category_source.name == 'test'
    assert response.status_code == 302


@pytest.mark.django_db
def test_category_delete(fixed_cost_category, fixed_cost_category_source):
    c = Client()
    c.force_login(fixed_cost_category.user)
    assert FixedCostSource.objects.count() == 1
    fixed_cost_category_source.delete()
    assert FixedCostSource.objects.count() == 0


'''////////////////VARIABLE COST CATEGORIES TESTS////////////////'''


@pytest.mark.django_db
def test_category_details_get(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    response = c.get(reverse('variable_category_details', kwargs={'id': variable_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_edit_get(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    response = c.get(reverse('variable_category_edit', kwargs={'id': variable_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_edit_post(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    assert variable_cost_category.name == 'blee'
    response = c.post(reverse('variable_category_edit', kwargs={'id': variable_cost_category.id}), {'name': 'test'})
    variable_cost_category.refresh_from_db()
    assert variable_cost_category.name == 'test'
    assert response.status_code == 302


@pytest.mark.django_db
def test_category_delete(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    assert VariableCostSourceCategory.objects.count() == 1
    variable_cost_category.delete()
    assert VariableCostSourceCategory.objects.count() == 0


@pytest.mark.django_db
def test_source_add_get(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    response = c.get(reverse('variable_add_source', kwargs={'id': variable_cost_category.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_source_add_post(variable_cost_category):
    c = Client()
    c.force_login(variable_cost_category.user)
    assert VariableCostSource.objects.count() == 0
    response = c.post(reverse('variable_add_source', kwargs={'id': variable_cost_category.id}), {'name': 'test'})
    assert response.status_code == 302
    assert VariableCostSource.objects.count() == 1


@pytest.mark.django_db
def test_category_source_edit_get(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category.user)
    response = c.get(reverse('variable_source_edit', kwargs={'id': variable_cost_category_source.id}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_source_edit_post(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category.user)
    assert variable_cost_category_source.name == 'bleeh'
    response = c.post(reverse('variable_source_edit', kwargs={'id': variable_cost_category_source.id}), {'name': 'test'})
    variable_cost_category_source.refresh_from_db()
    assert variable_cost_category_source.name == 'test'
    assert response.status_code == 302


@pytest.mark.django_db
def test_category_delete(variable_cost_category, variable_cost_category_source):
    c = Client()
    c.force_login(variable_cost_category.user)
    assert VariableCostSource.objects.count() == 1
    variable_cost_category_source.delete()
    assert VariableCostSource.objects.count() == 0