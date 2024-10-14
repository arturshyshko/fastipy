from authentication.constants import AuthException
from authentication.models import User


class TestRegisterUserViaEmailPasswordView:
    def test_successful_response(self, client, mocker):
        mocker.patch(
            "authentication.services.auth.AuthenticationService.register", return_value=User(email="test123@gmail.com")
        )

        resp = client.post(
            "/api/v1/auth/register",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        assert resp.status_code == 201
        assert resp.json() == {"email": "test123@gmail.com"}

    def test_auth_called(self, client, mocker):
        register_bl = mocker.patch("authentication.services.auth.AuthenticationService.register")

        client.post(
            "/api/v1/auth/register",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        register_bl.assert_called_once_with(email="test123@gmail.com", password="whatev1r")

    def test_errors_on_duplicate_user(self, client, mocker):
        mocker.patch(
            "authentication.services.auth.AuthenticationService.register",
            side_effect=AuthException("lol"),
        )

        resp = client.post(
            "/api/v1/auth/register",
            data={"email": "test123@gmail.com", "password": "whatev1r"},
            content_type="application/json",
        )

        assert resp.status_code == 400
        assert resp.json() == {"detail": "lol"}
