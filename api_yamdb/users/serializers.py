from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import AccessToken

from users.utils import generate_activation_code

User = get_user_model()
username_validator = UnicodeUsernameValidator()


def validate_username_include_me(value):
    if value == 'me':
        raise serializers.ValidationError(
            "Использовать имя 'me' в качестве username запрещено")
    return value


class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     validators=[username_validator,
                                                 validate_username_include_me])
    email = serializers.EmailField(max_length=254, validators=[validate_email])

    def validate(self, attrs):
        """Валидатор для создания пользователей.
        1. Если пользователь существует,
          то ему необходимо отправить новый код подтверждения:
          Осуществляется на основе отправленной модели пользователя
          в validated_data;
        2. Email текущего пользователя должен совподать
          с отправленными данными;
        3. Для нового пользователя email уникален.
        """
        username = attrs.get('username')
        email = attrs.get('email')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'email': f'{email=} уже используется'})
            return attrs
        if user.email == email:
            return user
        else:
            raise serializers.ValidationError(
                {'email': 'Укажите корректный адрес электронной почты'})

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        return validate_username_include_me(value)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound(f'User {data["username"]} does not exist')
        access_token = AccessToken.for_user(user)
        to_be_activation_code = generate_activation_code(
            self.initial_data['username'])
        if to_be_activation_code != data['confirmation_code']:
            raise serializers.ValidationError(
                {'confirmation_code': 'Value is invalid'})
        return {'token': str(access_token)}
