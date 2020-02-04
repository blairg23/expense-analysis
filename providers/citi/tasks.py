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
            transaction_date = get_date(date_string=transaction.get('Date'), date_format='%Y-%m-%d')
            post_date = transaction_date
            debit = float(transaction.get('Debit'))
            credit = float(transaction.get('Credit'))
            amount = debit + credit
            accounting_type = 'debit' if debit > 0 else 'credit'
            semantic_type = 'expense' if accounting_type == 'debit' else 'payment'
            categories = [transaction.get('Category')]

            transaction_dict = {
                "owner": owner,
                "source": 'citi',
                "transaction_date": transaction_date,
                "post_date": post_date,
                "amount": abs(amount),
                "description": transaction.get('Description'),
                "accounting_type": accounting_type,
                "semantic_type": semantic_type,
                "category": categories,
            }
            transformed_transactions.append(transaction_dict)
        except Exception as error:
            print(f'An error occurred: {error}')
            print('Transactions:\n')
            print(transaction)

    return transformed_transactions
