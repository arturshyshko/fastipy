import logging

import django.db.utils
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

import authentication.constants.errors as error_texts
from authentication.constants import AuthException
from authentication.models import User

logger = logging.getLogger(__name__)


class AuthenticationService:
    def register(self, email: str, password: str):
        logger.info("[Auth]: Registering user %s.", email)
        try:
            return User.objects.create_user(email, password=password)
        except django.db.utils.IntegrityError as e:
            raise AuthException(error_texts.AUTH_EMAIL_EXISTS) from e

    # Using Token auth for now for simplicity. Need to decide if we want to use Session or JWT or smth else later on.
    def login(self, email: str, password: str):
        logger.info("[Auth]: Logging in user %s.", email)
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return user, token
        else:
            raise AuthException(error_texts.AUTH_INVALID_CREDENTIALS)

    def logout(self, email: str):
        logger.info("[Auth]: Logging out user %s.", email)
        num_deleted, _ = Token.objects.filter(user__email=email).delete()
        return bool(num_deleted)
