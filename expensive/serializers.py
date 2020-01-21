import json

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from django.utils.text import slugify
# from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


from expensive.models import UserType, ExtendedUser, TransactionType, Category, Source, Transaction


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = [
            'id',
            'name',
            'description'
        ]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('email', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class ExtendedUserSerializer(serializers.ModelSerializer):
    type = UserTypeSerializer(read_only=True)

    class Meta:
        model = ExtendedUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'slug',
            'email',
            'mobile',
            'type',
        ]


class UserTypeField(serializers.Field):
    def to_internal_value(self, data):
        return UserType.objects.filter(id=data.get('id')).first()

    def to_representation(self, value):
        return UserTypeSerializer(value).data


class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()
    type = UserTypeField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = ExtendedUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'type',
            'password1',
            'password2',
        ]

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')

        if password1 != password2:
            raise Exception(message='Passwords do not match')

        person = ExtendedUser.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            mobile=validated_data.get('mobile'),
            username=validated_data.get('email'),
            type=validated_data.get('type')
        )
        person.set_password(password1)
        person.save()
        return person


class TransactionTypeSerializer(serializers.Serializer):
    transaction_type = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = TransactionType
        fields = '__all__'


class CategorySerializer(serializers.Serializer):
    category = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Category
        fields = '__all__'


class SourceSerializer(serializers.Serializer):
    source = serializers.CharField()

    class Meta:
        model = Source
        fields = '__all__'


class TransactionSerializer(serializers.Serializer):
    owner = PersonSerializer()
    source = SourceSerializer()
    transaction_date = serializers.DateField()
    post_date = serializers.DateField()
    amount = serializers.FloatField()
    description = serializers.CharField()
    category = CategorySerializer(many=True)
    type = TransactionTypeSerializer()

    class Meta:
        model = Category
        fields = '__all__'
