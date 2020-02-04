from server.celery import app

from expensive.models import TransactionType, Category, Source, Transaction
from expensive.utils import get_date
from expensive.serializers import ExtendedUserSerializer, TransactionTypeSerializer

# SOURCE, created = Source.objects.get_or_create(source='capitalone')


@app.task(ignore_result=True)
def transform_transactions(owner, transactions):
    """
    :param ExtendedUser owner: The owner of the transactions being transformed.
    :param list transactions: A list of transactions to transform.
    """
    transformed_transactions = []
    for transaction in transactions:
        categories = []
        if transaction.get('ActivityDate') is not None:
            transaction_date = get_date(date_string=transaction.get('ActivityDate'), date_format='%Y-%m-%d')
            post_date = transaction_date
            amount = float(transaction.get('Amount'))
            accounting_type = 'debit' if amount > 0 else 'credit'
            semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
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
            "owner": owner,
            "source": 'capitalone',
            "transaction_date": transaction_date,
            "post_date": post_date,
            "amount": abs(amount),
            "description": transaction.get('Description'),
            "accounting_type": accounting_type,
            "semantic_type": semantic_type,
            "category": categories,
        }
        transformed_transactions.append(transaction_dict)

    return transformed_transactions
