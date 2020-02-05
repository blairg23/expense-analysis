from expensive.models import Transaction, ExtendedUser
from django.db.models import Sum, Avg

start_date = '2019-09-01'
end_date = '2019-09-30'
owner = ExtendedUser.objects.get(email='blair.gemmer@gmail.com')

capitalone = Transaction.objects.filter(
    owner=owner,
    source__source='capitalone',
    post_date__gte=start_date,
    post_date__lte=end_date
).all()


chase = Transaction.objects.filter(
    owner=owner,
    source__source='chase',
    post_date__gte=start_date,
    post_date__lte=end_date
).all()

citi = Transaction.objects.filter(
    owner=owner,
    source__source='citi',
    post_date__gte=start_date,
    post_date__lte=end_date
).all()

discover = Transaction.objects.filter(
    owner=owner,
    source__source='discover',
    post_date__gte=start_date,
    post_date__lte=end_date
).all()

parksidefcu = Transaction.objects.filter(
    owner=owner,
    source__source='parksidefcu',
    post_date__gte=start_date,
    post_date__lte=end_date
).all()


#
# Capital One
#
capitalone_total = capitalone.aggregate(total=Sum('amount'), average=Avg('amount'))

if capitalone_total.get('total') is not None:
    try:
        capitalone_total_debits = capitalone.filter(accounting_type__transaction_type='debit').aggregate(total=Sum('amount'), average=Avg('amount'))
        capitalone_total_expenses = capitalone.filter(semantic_type__transaction_type='expense').aggregate(total=Sum('amount'), average=Avg('amount'))
        capitalone_total_credits = capitalone.filter(accounting_type__transaction_type='credit').aggregate(total=Sum('amount'), average=Avg('amount'))
        capitalone_total_payments = capitalone.filter(semantic_type__transaction_type='payment').aggregate(total=Sum('amount'), average=Avg('amount'))

        print('Capital One:')
        print(f'Total: ${capitalone_total}')
        print(f'Total Debits: ${capitalone_total_debits}')
        print(f'Total Expenses: ${capitalone_total_expenses}')
        print(f'Total Credits: ${capitalone_total_credits}')
        print(f'Total Payments: ${capitalone_total_payments}\n')
        print(f"Difference: ${capitalone_total_expenses.get('total') - capitalone_total_payments.get('total')}")
    except TypeError as error:
        print(f"Total Expenses: {capitalone_total_expenses.get('total')}")
        print(f"Total Payments: {capitalone_total_payments.get('total')}")


#
# Chase
#
chase_total = chase.aggregate(total=Sum('amount'), average=Avg('amount'))

if chase_total.get('total') is not None:
    try:
        chase_total_debits = chase.filter(accounting_type__transaction_type='debit').aggregate(total=Sum('amount'), average=Avg('amount'))
        chase_total_expenses = chase.filter(semantic_type__transaction_type='expense').aggregate(total=Sum('amount'), average=Avg('amount'))
        chase_total_credits = chase.filter(accounting_type__transaction_type='credit').aggregate(total=Sum('amount'), average=Avg('amount'))
        chase_total_payments = chase.filter(semantic_type__transaction_type='payment').aggregate(total=Sum('amount'), average=Avg('amount'))

        print('Chase:')
        print(f'Total: ${chase_total}')
        print(f'Total Debits: ${chase_total_debits}')
        print(f'Total Expenses: ${chase_total_expenses}')
        print(f'Total Credits: ${chase_total_credits}')
        print(f'Total Payments: ${chase_total_payments}')
        print(f"Difference: ${chase_total_expenses.get('total') - chase_total_payments.get('total')}\n")
    except TypeError as error:
        print(f"Total Expenses: {chase_total_expenses.get('total')}")
        print(f"Total Payments: {chase_total_payments.get('total')}")


#
# Citi
#
citi_total = citi.aggregate(total=Sum('amount'), average=Avg('amount'))

if citi_total.get('total') is not None:
    try:
        citi_total_debits = citi.filter(accounting_type__transaction_type='debit').aggregate(total=Sum('amount'), average=Avg('amount'))
        citi_total_expenses = citi.filter(semantic_type__transaction_type='expense').aggregate(total=Sum('amount'), average=Avg('amount'))
        citi_total_credits = citi.filter(accounting_type__transaction_type='credit').aggregate(total=Sum('amount'), average=Avg('amount'))
        citi_total_payments = citi.filter(semantic_type__transaction_type='payment').aggregate(total=Sum('amount'), average=Avg('amount'))

        print('Citi:')
        print(f'Total: ${citi_total}')
        print(f'Total Debits: ${citi_total_debits}')
        print(f'Total Expenses: ${citi_total_expenses}')
        print(f'Total Credits: ${citi_total_credits}')
        print(f'Total Payments: ${citi_total_payments}')
        print(f"Difference: ${citi_total_expenses.get('total') - citi_total_payments.get('total')}\n")
    except TypeError as error:
        print(f"Total Expenses: {citi_total_expenses.get('total')}")
        print(f"Total Payments: {citi_total_payments.get('total')}")
#
# Discover
#
discover_total = discover.aggregate(total=Sum('amount'), average=Avg('amount'))

if discover_total.get('total') is not None:
    try:
        discover_total_debits = discover.filter(accounting_type__transaction_type='debit').aggregate(total=Sum('amount'), average=Avg('amount'))
        discover_total_expenses = discover.filter(semantic_type__transaction_type='expense').aggregate(total=Sum('amount'), average=Avg('amount'))
        discover_total_credits = discover.filter(accounting_type__transaction_type='credit').aggregate(total=Sum('amount'), average=Avg('amount'))
        discover_total_payments = discover.filter(semantic_type__transaction_type='payment').aggregate(total=Sum('amount'), average=Avg('amount'))

        print('Discover:')
        print(f'Total: ${discover_total}')
        print(f'Total Debits: ${discover_total_debits}')
        print(f'Total Expenses: ${discover_total_expenses}')
        print(f'Total Credits: ${discover_total_credits}')
        print(f'Total Payments: ${discover_total_payments}')
        print(f"Difference: ${discover_total_expenses.get('total') - discover_total_payments.get('total')}\n")
    except TypeError as error:
        print(f"Total Expenses: {discover_total_expenses.get('total')}")
        print(f"Total Payments: {discover_total_payments.get('total')}")

#
# Parkside FCU
#
parksidefcu_total = parksidefcu.aggregate(total=Sum('amount'), average=Avg('amount'))

if parksidefcu_total.get('total') is not None:
    try:
        parksidefcu_total_debits = parksidefcu.filter(accounting_type__transaction_type='debit').aggregate(total=Sum('amount'), average=Avg('amount'))
        parksidefcu_total_expenses = parksidefcu.filter(semantic_type__transaction_type='expense').aggregate(total=Sum('amount'), average=Avg('amount'))
        parksidefcu_total_credits = parksidefcu.filter(accounting_type__transaction_type='credit').aggregate(total=Sum('amount'), average=Avg('amount'))
        parksidefcu_total_payments = parksidefcu.filter(semantic_type__transaction_type='payment').aggregate(total=Sum('amount'), average=Avg('amount'))

        print('Parkside FCU:')
        print(f'Total: ${parksidefcu_total}')
        print(f'Total Debits: ${parksidefcu_total_debits}')
        print(f'Total Expenses: ${parksidefcu_total_expenses}')
        print(f'Total Credits: ${parksidefcu_total_credits}')
        print(f'Total Payments: ${parksidefcu_total_payments}')
        print(f"Difference: ${parksidefcu_total_expenses.get('total') - parksidefcu_total_payments.get('total')}\n")
    except TypeError as error:
        print(f"Total Expenses: {parksidefcu_total_expenses.get('total')}")
        print(f"Total Payments: {parksidefcu_total_payments.get('total')}")