from server.celery import app

from expensive.models import TransactionType, Category, Source, Transaction
from expensive.utils import get_date

SOURCE, created = Source.objects.get_or_create(source='chase')


@app.task(ignore_result=True)
def import_transactions(owner, transactions_dict):
    transactions = []
    for transaction in transactions_dict:
        transaction_date = get_date(date_string=transaction.get('Transaction Date'), date_format='%Y-%m-%d')
        post_date = get_date(date_string=transaction.get('Post Date'), date_format='%Y-%m-%d')
        amount = float(transaction.get('Amount'))
        transaction_category1, created = Category.objects.get_or_create(category=transaction.get('Category', 'None'))
        transaction_category2, created = Category.objects.get_or_create(category=transaction.get('Type', 'None'))
        transaction_type_name = 'credit' if amount > 0 else 'debit'
        transaction_type, created = TransactionType.objects.get_or_create(transaction_type=transaction_type_name)

        transaction_object, created = Transaction.objects.get_or_create(
            owner=owner,
            source=SOURCE,
            transaction_date=transaction_date,
            post_date=post_date,
            amount=amount,
            description=transaction.get('Description'),
            type=transaction_type
        )

        if created:
            transaction_object.category.add(transaction_category1)
            transaction_object.category.add(transaction_category2)

        transactions.append(transaction_object)

    return transactions
