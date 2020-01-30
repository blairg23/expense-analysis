from server.celery import app

from expensive.models import TransactionType, Category, Source, Transaction
from expensive.utils import get_date

SOURCE, created = Source.objects.get_or_create(source='capitalone')


@app.task(ignore_result=True)
def import_transactions(owner, transactions_dict):
    transactions = []

    for transaction in transactions_dict:
        # If we're looking at a pre-2018 era transaction list:
        if transaction.get('ActivityDate') is not None:
            transaction_date = get_date(date_string=transaction.get('ActivityDate'), date_format='%Y-%m-%d')
            post_date = transaction_date
            amount = float(transaction.get('Amount'))
            transaction_type_name = 'debit' if amount > 0 else 'credit'
            transaction_type, created = TransactionType.objects.get_or_create(transaction_type=transaction_type_name)
            transaction_category, created = Category.objects.get_or_create(category='None')
        else:
            transaction_date = get_date(date_string=transaction.get('Transaction Date'), date_format='%Y-%m-%d')
            post_date = get_date(date_string=transaction.get('Posted Date'), date_format='%Y-%m-%d')
            debit = float(transaction.get('Debit'))
            credit = float(transaction.get('Credit'))
            amount = None
            transaction_type_name = None
            transaction_type = None

            if debit == 0.0:
                transaction_type_name = 'credit'
                amount = float(credit)
            elif credit == 0.0:
                transaction_type_name = 'debit'
                amount = float(debit)

            if transaction_type_name is not None:
                transaction_type, created = TransactionType.objects.get_or_create(transaction_type=transaction_type_name)

            transaction_category, created = Category.objects.get_or_create(category=transaction.get('Category'))

        if transaction_type is not None:
            transaction_object, created = Transaction.objects.get_or_create(
                owner=owner,
                source=SOURCE,
                transaction_date=transaction_date,
                post_date=post_date,
                amount=abs(amount),
                description=transaction.get('Description'),
                type=transaction_type
            )

            if created:
                transaction_object.category.add(transaction_category)

            transactions.append(transaction_object)

    return transactions
