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
            if transaction.get('CR/DR') is not None:
                transaction_date = get_date(date_string=transaction.get('Posted Date'), date_format='%Y-%m-%d')
                post_date = transaction_date
                amount = float(transaction.get('Amount'))
                description = transaction.get("Description")
                accounting_type = 'debit' if transaction.get('CR/DR') == 'DR' else 'credit'
                semantic_type = 'income' if accounting_type == 'debit' else 'expense'
            else:
                transaction_date = get_date(date_string=transaction.get('Date'), date_format='%Y-%m-%d')
                post_date = transaction_date
                debit = abs(float(transaction.get('Amount Debit')))
                credit = abs(float(transaction.get('Amount Credit')))
                amount = debit + credit
                description = f"Description: {transaction.get('Description')}\nMemo: {transaction.get('Memo')}"
                accounting_type = 'debit' if debit > 0 else 'credit'
                semantic_type = 'income' if accounting_type == 'credit' else 'expense'

            transaction_dict = {
                "owner": owner,
                "source": 'parksidefcu',
                "transaction_date": transaction_date,
                "post_date": post_date,
                "amount": abs(amount),
                "description": description,
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
