from server.celery import app

from expensive.models import TransactionType, Category, Source, Transaction
from expensive.utils import get_date
from expensive.serializers import TransactionSerializer


@app.task(ignore_result=True)
def import_transactions(transactions):
    # source, created = Source.objects.get_or_create(source=source)
    # transactions = []

    transaction_serializer = TransactionSerializer(data=transactions, many=True)
    if transaction_serializer.is_valid(raise_exception=True):
        transactions = transaction_serializer.save()
    #     transaction_object, created = Transaction.objects.get_or_create(
    #         owner=owner,
    #         source=source,
    #         transaction_date=transaction.get('transaction_date'),
    #         post_date=transaction.get('post_date'),
    #         amount=transaction.get('amount'),
    #         description=transaction.get('description'),
    #         accounting_type=transaction.get('accounting_type'),
    #         semantic_type=transaction.get('semantic_type'),
    #     )
    #
    #     if created:
    #         for category in transaction.get('categories', []):
    #             transaction_object.category.add(category)
    #
    #     # transactions.append(transaction_object)
    #
    return transactions
