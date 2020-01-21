from django.apps import apps as django_apps


def get_model(app_dot_model: str):
    """Get a Django model using Django internals. This utility is helpful for preventing circular
    imports.

    :param app_dot_model: Django app label & Django model name, separated by a dot. Example: "auth.User".
    :return: Django model class
    """

    app_label, model_name = app_dot_model.split(".")

    return django_apps.get_app_config(app_label).get_model(model_name)