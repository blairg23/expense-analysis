from server.celery import app

from expensive.models import TransactionType, Source, Transaction


@app.task(ignore_result=True)
def import_transactions(transformed_transactions):
    """
    :param list transformed_transactions: A list of transformed transactions to add to the database.
    """
    transactions = []

    # TODO: Get serializers working
    # transaction_serializer = TransactionSerializer(data=transactions, many=True)
    # if transaction_serializer.is_valid(raise_exception=True):
    #     transactions = transaction_serializer.save()

    for transaction in transformed_transactions:
        source = transaction.get('source')
        accounting_type = transaction.get('accounting_type')
        semantic_type = transaction.get('semantic_type')

        source, created = Source.objects.get_or_create(source=source)
        accounting_type, created = TransactionType.objects.get_or_create(
            transaction_type=accounting_type,
            defaults={
                "transaction_type": accounting_type,
                "description": accounting_type
            }
        )
        semantic_type, created = TransactionType.objects.get_or_create(
            transaction_type=semantic_type,
            defaults={
                "transaction_type": semantic_type,
                "description": semantic_type
            }
        )

        transaction_object, created = Transaction.objects.get_or_create(
            owner=transaction.get('owner'),
            source=source,
            transaction_date=transaction.get('transaction_date'),
            post_date=transaction.get('post_date'),
            amount=transaction.get('amount'),
            description=transaction.get('description'),
            accounting_type=accounting_type,
            semantic_type=semantic_type,
        )

        if created:
            for category in transaction.get('categories', []):
                transaction_object.category.add(category)

        transactions.append(transaction_object)

    return transactions


@app.task(ignore_result=True)
def verify_imported_transactions(transformed_transactions, imported_transactions):
    transformed_amount = 0
    for transaction in transformed_transactions:
        transformed_amount += transaction.get('amount')

    imported_amount = 0
    dates = []
    for transaction in imported_transactions:
        imported_amount += transaction.amount
        dates.append(transaction.post_date)

    verified_transactions = {
        "transformed_amount": transformed_amount,
        "imported_amount": imported_amount,
        "min_date": min(dates),
        "max_date": max(dates),
    }

    return verified_transactions