"""Django REST Framework ViewSets for `expensive`."""

from django.conf import settings
from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from expensive import serializers
from expensive import permissions
from expensive.models import Transaction
from expensive.utils import get_model, get_transactions
from expensive.tasks import import_transactions, verify_imported_transactions

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
            transactions = get_transactions(transactions_dataframe=transactions_dataframe)  # json.loads(transactions_dataframe.to_json())

            if provider not in settings.SUPPORTED_PROVIDERS:
                return Response({'error': f'provider not found, choose from: {settings.SUPPORTED_PROVIDERS}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                transformed_transactions = getattr(getattr(getattr(providers, provider), "tasks"), "transform_transactions")(owner=current_user, transactions=transactions)
                imported_transactions = import_transactions(transformed_transactions=transformed_transactions)
                verified_transactions = verify_imported_transactions(transformed_transactions=transformed_transactions, imported_transactions=imported_transactions)
                # getattr(getattr(getattr(providers, provider), "tasks"), "import_transactions")(owner=current_user, transactions_dict=transactions_dict)
                # reduce(getattr, f"{provider}.tasks.import_transactions".split("."), providers)(owner=current_user, transactions_dict=transactions_dict)
                min_date = verified_transactions.get('min_date')
                max_date = verified_transactions.get('max_date')
                database_amount = Transaction.objects.filter(
                    owner=current_user,
                    source__source=provider,
                    post_date__gte=min_date,
                    post_date__lte=max_date
                ).aggregate(amount=Sum('amount')).get('amount')

                transformed_amount = verified_transactions.get('transformed_amount')
                imported_amount = verified_transactions.get('imported_amount')
                transformed_transactions = verified_transactions.get('transformed_transactions')
                imported_transactions = verified_transactions.get('imported_transactions')
                num_dates = verified_transactions.get('num_dates')

                if transformed_amount == imported_amount == database_amount:
                    response_message = f"Data imported successfully 100%, amount imported: ${database_amount}\n"
                else:
                    response_message = f"Data import unsuccessful, {transformed_amount / database_amount if database_amount is not None else 0}%\n"
                    response_message += f"Original Amount: ${transformed_amount}\n"
                    response_message += f"Amount after import: ${imported_amount}\n"
                    response_message += f"Amount in database: ${database_amount}\n"
                    response_message += f"Original number of transactions: {len(transactions)}\n"
                    response_message += f"Number of transformed transactions: {transformed_transactions}\n"
                    response_message += f"Number of imported transactions: {imported_transactions}\n"
                    response_message += f"Number of imported dates: {num_dates}\n"

                    all_transactions = Transaction.objects.filter(
                        owner=current_user,
                        source__source=provider,
                        post_date__gte=min_date,
                        post_date__lte=max_date,
                    ).all()

                    response_message += f"Number of database transactions: {all_transactions.count()}\n"

                    # for transaction in all_transactions:
                    #     print(transaction)

                print(response_message)

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
