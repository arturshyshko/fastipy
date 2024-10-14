from rest_framework.authtoken.models import Token

from authentication.constants import AuthException
from authentication.models import User


class TestLoginUserViaEmailPasswordView:
    def test_successful_response(self, client, mocker):
        user = User(email="test123@gmail.com")
        mocker.patch(
            "authentication.services.auth.AuthenticationService.login",
            return_value=(user, Token(key="sometoken", user=user)),
        )
        resp = client.post(
            "/api/v1/auth/login",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        assert resp.status_code == 200
        assert resp.json() == {"token": "sometoken"}

    def test_auth_called(self, client, mocker):
        user = User(email="test123@gmail.com")
        login_bl = mocker.patch(
            "authentication.services.auth.AuthenticationService.login",
            return_value=(user, Token(key="sometoken", user=user)),
        )

        client.post(
            "/api/v1/auth/login",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        login_bl.assert_called_once_with(email="test123@gmail.com", password="whatev1r")

    def test_errors_on_duplicate_user(self, client, mocker):
        mocker.patch(
            "authentication.services.auth.AuthenticationService.login",
            side_effect=AuthException("lol"),
        )

        resp = client.post(
            "/api/v1/auth/login",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        assert resp.status_code == 400
        assert resp.json() == {"detail": "lol"}
