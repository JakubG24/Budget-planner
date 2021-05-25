import pytest
from django.contrib.auth.models import User

from income.models import IncomeSourceCategory, IncomeSource, Income


@pytest.fixture
def user():
    u = User()
    u.username = 'kubaa'
    u.set_password('kubaa')
    u.save()
    return u


@pytest.fixture
def category(user):
    c = IncomeSourceCategory.objects.create(name='blee', user=user)
    return c


@pytest.fixture
def category_source(category):
    cs = IncomeSource.objects.create(name='blee', user=category.user)
    cs.sources.add(category)
    return cs
