from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import UserSerializer
from authentication.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=["get"], url_path="me", url_name="me", permission_classes=[IsAuthenticated])
    def get_current_user(self, request, pk=None):
        """Return currently logged-in user"""
        self.kwargs["pk"] = self.request.user.pk
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
