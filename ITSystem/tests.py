import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from ITSystem.models import Ticket, Category


@pytest.mark.django_db
def test_ticket_creation():

    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

    category = Category.objects.create(
        name='Software Issue'
    )

    ticket = Ticket.objects.create(
        title='Login Problem',
        description='Cannot login',
        due_date='2026-05-20',
        priority='High',
        status='Open',
        category=category,
        created_by=user
    )

    assert ticket.title == 'Login Problem'


@pytest.mark.django_db
def test_login_page_loads(client):

    response = client.get(
        reverse('login')
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_login(client):

    User.objects.create_user(
        username='usama',
        password='test12345'
    )

    response = client.post(
        reverse('login'),
        {
            'username': 'usama',
            'password': 'test12345'
        }
    )

    assert response.status_code == 302

    