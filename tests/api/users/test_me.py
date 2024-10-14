import pytest

from authentication.models import User


@pytest.mark.django_db
class TestUsersMeView:
    def test_returns_correct_user(self, client):
        correct_user = User.objects.create(email="test@gmail.com")
        User.objects.create(email="test2@gmail.com")  # Other user in the system.

        client.force_login(correct_user)
        resp = client.get("/api/v1/users/me/")

        assert resp.status_code == 200
        assert resp.json()["id"] == str(correct_user.pk)
