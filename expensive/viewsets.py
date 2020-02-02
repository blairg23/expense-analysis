"""Django REST Framework ViewSets for `expensive`."""
import numpy
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from expensive import serializers
from expensive import permissions
from expensive.serializers import TransactionSerializer
from expensive.utils import get_model, get_transactions_dict
from expensive.tasks import import_transactions

import providers

from functools import reduce
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

    @action(detail=False, methods=['options', 'post'])
    def upload_files(self, request):
        current_user = request.user
        provider = request.POST.get('provider')
        csv_files = request.FILES.getlist('csv_file')

        for csv_file in csv_files:
            print(f'Processing {csv_file}...')
            transactions_dataframe = pandas.read_csv(csv_file, thousands=',')
            transactions_dataframe.fillna(0, inplace=True)
            transactions_dict = get_transactions_dict(transactions_dataframe=transactions_dataframe)  # json.loads(transactions_dataframe.to_json())

            if provider not in settings.SUPPORTED_PROVIDERS:
                return Response({'error': f'provider not found, choose from: {settings.SUPPORTED_PROVIDERS}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                getattr(getattr(getattr(providers, provider), "tasks"), "modify_transactions_dict")(transactions_dict=transactions_dict)
                import_transactions(source=provider, owner=current_user, transactions_dict=transactions_dict)
                # getattr(getattr(getattr(providers, provider), "tasks"), "import_transactions")(owner=current_user, transactions_dict=transactions_dict)
                # reduce(getattr, f"{provider}.tasks.import_transactions".split("."), providers)(owner=current_user, transactions_dict=transactions_dict)

                response = Response("File(s) Uploaded Successfully!", status=status.HTTP_200_OK)

        return response

    # @action(detail=False, methods=['options', 'get'])
    # def monthly_report(self, request):
    #     response = []
    #     valid_transactions = []
    #     start_date = request.query_params.get('start_date')
    #     end_date = request.query_params.get('end_date')
    #     transactions = get_model("expensive.Transaction").objects.filter(owner=self.request.user, post_date__gte=start_date, post_date__lte=end_date)
    #     for transaction in transactions:
    #         transaction_data = {
    #
    #         }
        #     transaction_serializer = TransactionSerializer(data=transaction)
        #     # print(transaction_serializer.is_valid())
        #     print(transaction_serializer.initial_data())
        #     if transaction_serializer.is_valid():
        #         valid_transactions.append(transaction_serializer.data())
        #
        # return Response(valid_transactions, status=status.HTTP_200_OK)
