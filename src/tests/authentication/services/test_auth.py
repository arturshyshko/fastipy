import pytest
from rest_framework.authtoken.models import Token

import authentication.constants.errors as errors_text
from authentication.constants.exceptions import AuthException
from authentication.models import User
from authentication.services import AuthenticationService


@pytest.mark.django_db
class TestAuthenticationServiceRegister:
    def test_register_successful(self):
        AuthenticationService().register(email="test123@gmail.com", password="whatever")

        result = User.objects.get(email="test123@gmail.com")

        assert result.email == "test123@gmail.com"

    def test_raises_on_duplicate_email(self):
        User.objects.create_user("test123@gmail.com", password="whatever")

        with pytest.raises(AuthException, match=errors_text.AUTH_EMAIL_EXISTS):
            AuthenticationService().register(email="test123@gmail.com", password="whatever2")


@pytest.mark.django_db
class TestAuthenticationServiceLogin:
    def test_login_successful(self):
        user = User.objects.create_user("test123@gmail.com", password="whatever")

        user, token = AuthenticationService().login(email="test123@gmail.com", password="whatever")

        assert user == user
        assert token.user == user

    def test_login_incorrect_password_fails(self):
        user = User.objects.create_user("test123@gmail.com", password="whatever")

        with pytest.raises(AuthException, match=errors_text.AUTH_INVALID_CREDENTIALS):
            AuthenticationService().login(email="test123@gmail.com", password="whatever2")
        assert len(Token.objects.filter(user_id=user.pk)) == 0

    def test_login_nonexistent_user_fails(self):
        with pytest.raises(AuthException, match=errors_text.AUTH_INVALID_CREDENTIALS):
            AuthenticationService().login(email="test123@gmail.com", password="whatever")
