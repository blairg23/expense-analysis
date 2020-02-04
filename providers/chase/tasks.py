from server.celery import app

from expensive.utils import get_date


@app.task(ignore_result=True)
def transform_transactions(owner, transactions):
    """
    :param ExtendedUser owner: The owner of the transactions being transformed.
    :param list transactions: A list of transactions to transform.
    """
    transformed_transactions = []
    for transaction in transactions:
        transaction_date = get_date(date_string=transaction.get('Transaction Date'), date_format='%Y-%m-%d')
        post_date = get_date(date_string=transaction.get('Post Date'), date_format='%Y-%m-%d')
        amount = float(transaction.get('Amount'))
        accounting_type = 'credit' if amount > 0 else 'debit'
        semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
        category1 = transaction.get('Category')
        category2 = transaction.get('Type')
        categories = [category1, category2]

        transaction_dict = {
            "owner": owner,
            "source": 'chase',
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
