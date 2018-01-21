import json

from django.utils.text import slugify
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from expensive.models import UserType, ExtendedUser


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = [
            'id',
            'name',
            'description'
        ]


class ExtendedUserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        fields = '__all__'

    def save(self, request):
        request['username'] = request.data['email']
        user = super(ExtendedRegisterSerializer, self).save(request)
        user.set_password(request.data['password1'])
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
    type = UserTypeField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.EmailField()

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
