import pytest
from django.contrib.auth.models import User

from expense.models import FixedCostSourceCategory, FixedCostSource, VariableCostSourceCategory, VariableCostSource


@pytest.fixture
def user():
    u = User()
    u.username = 'kubaa'
    u.set_password('kubaa')
    u.save()
    return u


@pytest.fixture
def fixed_cost_category(user):
    result = FixedCostSourceCategory.objects.create(name='blee', user=user)
    return result


@pytest.fixture
def fixed_cost_category_source(fixed_cost_category):
    result = FixedCostSource.objects.create(name='bleeh', user=fixed_cost_category.user, source=fixed_cost_category)
    return result


@pytest.fixture
def variable_cost_category(user):
    result = VariableCostSourceCategory.objects.create(name='blee', user=user)
    return result


@pytest.fixture
def variable_cost_category_source(variable_cost_category):
    result = VariableCostSource.objects.create(name='bleeh', user=variable_cost_category.user,
                                               source=variable_cost_category)
    return result
