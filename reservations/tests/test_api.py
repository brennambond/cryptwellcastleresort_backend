import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_reservation_list_authenticated_user():
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',  # ✅ New: email is provided
        password='testpass'
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse("list_user_reservations"))

    assert response.status_code == 200
