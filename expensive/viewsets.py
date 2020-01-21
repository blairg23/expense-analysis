"""Django REST Framework ViewSets for `expensive`."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from expensive import serializers
from expensive import permissions
from expensive.utils import get_model


class TransactionViewSet(ModelViewSet):
    """ViewSet of the `reservation.Location` Django model."""

    http_method_names = ["get", "post"]
    lookup_field = "owner__slug"
    lookup_url_kwarg = "user_id"
    permission_classes = [IsAuthenticated, permissions.IsDeveloper]
    queryset = get_model("expensive.Transaction").objects.all()
    serializer_class = serializers.TransactionSerializer
    filter_fields = ["created", "updated"]