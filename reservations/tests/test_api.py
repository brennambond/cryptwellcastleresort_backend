import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_reservation_list_authenticated_user():
    client = APIClient()
    response = client.get(reverse("reservation-list"))
    assert response.status_code == 200
