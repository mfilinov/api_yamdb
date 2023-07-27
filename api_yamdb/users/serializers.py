from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.utils import generate_activation_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено")
        return value


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
