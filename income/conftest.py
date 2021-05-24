import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user():
    u = User()
    u.username = 'kubaa'
    u.set_password('kubaa')
    u.save()
    return u