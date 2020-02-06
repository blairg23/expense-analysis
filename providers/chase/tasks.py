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
        try:
            categories = []
            transaction_date = get_date(date_string=transaction.get('Transaction Date'), date_format='%Y-%m-%d')
            post_date = get_date(date_string=transaction.get('Post Date'), date_format='%Y-%m-%d')
            amount = float(transaction.get('Amount'))
            accounting_type = 'credit' if amount > 0 else 'debit'
            semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
            category1 = transaction.get('Category')
            category2 = transaction.get('Type')
            for category in [category1, category2]:
                if category is not None:
                    categories.append(category)

            transaction_dict = {
                "owner": owner,
                "source": 'chase',
                "transaction_date": transaction_date,
                "post_date": post_date,
                "amount": abs(amount),
                "description": transaction.get('Description'),
                "accounting_type": accounting_type,
                "semantic_type": semantic_type,
                "categories": categories,
                "transaction": transaction,
            }
            transformed_transactions.append(transaction_dict)
        except Exception as error:
            print(f'An error occurred: {error}')
            print('Transaction:\n')
            print(transaction)

    return transformed_transactions
