from server.celery import app

from expensive.models import TransactionType, Category, Transaction
from expensive.utils import get_date
from expensive.serializers import ExtendedUserSerializer, TransactionTypeSerializer

# SOURCE, created = Source.objects.get_or_create(source='capitalone')


@app.task(ignore_result=True)
def transform_transactions(owner, transactions):
    """
    :param list transactions:
    """
    transformed_transactions = []
    categories = []
    for transaction in transactions:
        if transaction.get('ActivityDate') is not None:
            transaction_date = get_date(date_string=transaction.get('ActivityDate'), date_format='%Y-%m-%d')
            post_date = transaction_date
            amount = float(transaction.get('Amount'))
            accounting_type = 'debit' if amount > 0 else 'credit'
            semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
            debit = amount if accounting_type == 'debit' else 0.0
            credit = amount if accounting_type == 'credit' else 0.0
        else:
            transaction_date = get_date(date_string=transaction.get('Transaction Date'), date_format='%Y-%m-%d')
            post_date = get_date(date_string=transaction.get('Posted Date'), date_format='%Y-%m-%d')
            debit = float(transaction.get('Debit'))
            credit = float(transaction.get('Credit'))
            amount = debit + credit
            accounting_type = 'debit' if debit > 0 else 'credit'
            semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
            category = transaction.get('Category')
            if category is not None:
                categories.append(category)

        transaction_dict = {
            "owner": vars(owner),
            "source": {
                "source": "capitalone"
            },
            "transaction_date": transaction_date,
            "post_date": post_date,
            "debit": debit,
            "credit": credit,
            "amount": abs(amount),
            "description": transaction.get('Description'),
            "accounting_type": {
                "transaction_type": accounting_type,
                "description": accounting_type
            },
            "semantic_type": {
                "transaction_type": semantic_type,
                "description": semantic_type
            },
            "category": [
                {
                    "category": category,
                    "description": category
                }
                for category in categories
            ],
        }
        transformed_transactions.append(transaction_dict)

    return transformed_transactions


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
            amount = debit + credit
            transaction_type_name = None
            transaction_type = None

            if debit == 0.0:
                transaction_type_name = 'credit'
            elif credit == 0.0:
                transaction_type_name = 'debit'

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
