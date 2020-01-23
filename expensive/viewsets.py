"""Django REST Framework ViewSets for `expensive`."""
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from expensive import serializers
from expensive import permissions
from expensive.utils import get_model, get_transactions_dict

from providers.discover import tasks as discover_tasks

import pandas


class TransactionViewSet(ModelViewSet):
    """ViewSet of the `reservation.Location` Django model."""

    http_method_names = ["get", "options", "post"]
    permission_classes = [IsAuthenticated, permissions.IsDeveloper]
    # queryset = get_model("expensive.Transaction").objects.all()
    serializer_class = serializers.TransactionSerializer
    filter_fields = ["created", "updated"]

    def get_queryset(self):
        return get_model("expensive.Transaction").objects.filter(owner=self.request.user)

    @action(detail=True, methods=['options', 'post'])
    def upload_file(self, request, pk=None):
        provider = request.POST.get('provider')
        csv_file = request.FILES['csv_file']
        transactions_dataframe = pandas.read_csv(csv_file)
        transactions_dict = get_transactions_dict(transactions_dataframe=transactions_dataframe)# json.loads(transactions_dataframe.to_json())

        if provider not in settings.SUPPORTED_PROVIDERS:
            response = Response({'error': f'provider not found, choose from: {settings.SUPPORTED_PROVIDERS}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = discover_tasks.import_transactions(owner=request.user, transactions_dict=transactions_dict)
            # response = getattr(f'{provider}_tasks', 'import_transactions')(transactions_dict=transactions_dict)
            response = Response("File Uploaded Successfully!", status=status.HTTP_200_OK)

        return response