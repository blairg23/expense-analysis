from server.celery import app

from expensive.models import TransactionType, Category, Source, Transaction

SOURCE, created = Source.objects.get_or_create(source='discover')


@app.task(ignore_result=True)
def import_transactions(owner, transactions_dict):
    transactions = []
    for transaction in transactions_dict:
        amount = transaction.get('Amount')
        transaction_type_name = 'credit' if amount > 0 else 'debit'
        transaction_type = TransactionType.objects.get_or_create(transaction_type=transaction_type_name)

        transaction_object = Transaction.objects.create(
            owner=owner,
            source=SOURCE,
            transaction_date=transaction.get('Trans. Date'),
            post_date=transaction.get('Post Date'),
            amount=amount,
            description=transaction.get('Description'),
            category=transaction.get('Category'),
            type=transaction_type
        )

    transactions.append(transaction_object)

    return transactions
