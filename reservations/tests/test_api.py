import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_reservation_list_authenticated_user(authenticated_client):
    response = authenticated_client.get(reverse("list_user_reservations"))

    assert response.status_code == 200
