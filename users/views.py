from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .models import ConfirmationCode
from .serializers import UserAuthSerializer, UserCreateSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        User.objects.create_user(username=username, password=password)
        return Response(status=status.HTTP_201_CREATED)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        code = request.data.get('code')
        try:
            confirmation_code = ConfirmationCode.objects.get(code=code)
            if confirmation_code.is_expired():
                return Response(data={"error": "Confirmation code has expired. Please register again."},
                                status=status.HTTP_400_BAD_REQUEST)
            user = confirmation_code.user
            user.is_active = True
            user.save()
            return Response(data={"message": "User successfully confirmed."}, status=status.HTTP_200_OK)
        except ConfirmationCode.DoesNotExist:
            return Response(data={"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def confirm_user_api_view(request):
#     code = request.data.get('code')
#     try:
#         confirmation_code = ConfirmationCode.objects.get(code=code)
#         if confirmation_code.is_expired():
#             return Response(data={"error": "Confirmation code has expired. Please register again."},
#                             status=status.HTTP_400_BAD_REQUEST)
#         user = confirmation_code.user
#         user.is_active = True
#         user.save()
#         return Response(data={"message": "User successfully confirmed."}, status=status.HTTP_200_OK)
#     except ConfirmationCode.DoesNotExist:
#         return Response(data={"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
