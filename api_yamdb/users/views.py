from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from django.core.mail import send_mail

from users.models import User
from users.serializers import UserSerializer, TokenSerializer
from users.utils import generate_activation_code


class SignupViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        confirmation_code = generate_activation_code(response.data['username'])
        send_mail(
            subject='Register',
            message=f'Registration success, your {confirmation_code=}',
            from_email='yamdb@yamdb.ru',
            recipient_list=[response.data['email']],
            fail_silently=True)
        return response


class TokenView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
