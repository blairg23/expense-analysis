"""Factories for `expensive`."""

import factory
import pytz

from expensive import models


class UserTypeFactory(factory.DjangoModelFactory):
    """Factory for `expensive.UserType` Django model."""

    class Meta:
        model = models.UserType

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)


class ExtendedUserFactory(factory.DjangoModelFactory):
    """Factory for `expensive.ExtendedUser` Django model."""

    class Meta:
        model = models.ExtendedUser

    email = factory.Faker("email")
    username = email
    mobile = factory.Faker("phone_number")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    type = factory.SubFactory(UserTypeFactory)
    slug = factory.Faker("slug")
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)


class TransactionTypeFactory(factory.DjangoModelFactory):
    """Factory for `expensive.TransactionType` Django model."""

    class Meta:
        model = models.UserType

    transaction_type = factory.Iterator(["debit", "credit"])
    description = factory.Faker("word")
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)


class CategoryFactory(factory.DjangoModelFactory):
    """Factory for `expensive.Category` Django model."""

    class Meta:
        model = models.Category

    category = factory.Faker("word")
    description = factory.Faker("word")
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)


class SourceFactory(factory.DjangoModelFactory):
    """Factory for `expensive.Source` Django model."""

    class Meta:
        model = models.Source

    source = factory.Faker("word")
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)


class TransactionFactory(factory.DjangoModelFactory):
    """Factory for `expensive.Transaction` Django model."""

    class Meta:
        model = models.Transaction

    owner = factory.SubFactory(ExtendedUserFactory)
    source = factory.SubFactory(SourceFactory)
    transaction_date = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    post_date = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    amount = factory.Faker("pyfloat")
    description = factory.Faker("sentence")
    type = factory.SubFactory(TransactionTypeFactory)
    created = factory.Faker("past_datetime", tzinfo=pytz.UTC)
    updated = factory.Faker("past_datetime", tzinfo=pytz.UTC)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        """Add as many categories as you want"""
        if create and extracted:
            for _category in extracted:
                self.category.add(_category)
