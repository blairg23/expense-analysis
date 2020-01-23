from django.apps import apps as django_apps


def get_model(app_dot_model: str):
    """Get a Django model using Django internals. This utility is helpful for preventing circular
    imports.

    :param app_dot_model: Django app label & Django model name, separated by a dot. Example: "auth.User".
    :return: Django model class
    """

    app_label, model_name = app_dot_model.split(".")

    return django_apps.get_app_config(app_label).get_model(model_name)


def get_transactions_dict(transactions_dataframe):
    transactions_dict = []
    for index, row in transactions_dataframe.iterrows():
        # print('index:', index)
        # print('row:', row.index)
        temp_dict = {key: value for key, value in zip(row.index, row[row.index])}
        transactions_dict.append(temp_dict)
        # print(temp_dict)
        # print('\n')
        # temp_dict = {
        #     'transaction_date':
        # }
    #     counter += 1
    #     print(f"Trans. Date: {row['Trans. Date']}")
    #     print(f"Post Date: {row['Post Date']}")
    #     print(f"Description: {row['Description']}")
    #     print(f"Amount: {row['Amount']}")
    #     print(f"Category: {row['Category']}")
    #     print('\n')
    #
    # print(counter, ' entries')
    return transactions_dict