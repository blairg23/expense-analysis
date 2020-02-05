from django.apps import apps as django_apps

from dateutil.parser import parse
import datetime


def get_model(app_dot_model: str):
    """Get a Django model using Django internals. This utility is helpful for preventing circular
    imports.

    :param app_dot_model: Django app label & Django model name, separated by a dot. Example: "auth.User".
    :return: Django model class
    """

    app_label, model_name = app_dot_model.split(".")

    return django_apps.get_app_config(app_label).get_model(model_name)


def get_date(date_string, date_format):
    return datetime.datetime.strftime(parse(date_string), date_format)


def get_transactions(transactions_dataframe):
    """
    :params pandas.DataFrame transactions_dataframe: A Pandas DataFrame representing a CSV of transactions.
    """
    transactions = []
    for index, row in transactions_dataframe.iterrows():
        temp_dict = {str(key): str(value) for key, value in zip(row.index, row[row.index])}
        transactions.append(temp_dict)

    return transactions