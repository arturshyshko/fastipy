import pytest
from rest_framework.authtoken.models import Token

from authentication.models import User
from authentication.services import AuthenticationService


@pytest.mark.django_db
class TestLogout:
    def test_integration(self, client):
        user = User.objects.create_user("test@gmail.com", password="whatev1r")
        AuthenticationService().login(email=user.email, password="whatev1r")

        client.force_login(user)
        resp = client.delete("/api/v1/auth/logout")

        assert resp.status_code == 200

        assert Token.objects.filter(user_id=user.pk).count() == 0
