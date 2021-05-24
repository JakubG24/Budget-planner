import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from income.models import Income


@pytest.mark.django_db
def test_client():
    Client()


@pytest.mark.django_db
def test_get_user(user):
    users = User.objects.all()
    assert users.count() == 1


@pytest.mark.django_db
def test_index_view_get():
    c = Client()
    response = c.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_income_get_not_logged_in(user):
    c = Client()
    response = c.get(reverse('add_income'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_add_income_get_not_logged_in(user):
    c = Client()
    c.force_login(user)
    response = c.get(reverse('add_income'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_income_post(user):
    c = Client()
    c.force_login(user)
    response = c.post(reverse('add_income'), {'amount': 100, 'date': '05.05.2021', 'description': 'test', 'category': 'test',
                                              'source': 'test'})
    assert response.status_code == 302
    assert Income.objects.count() == 1
