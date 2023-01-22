from .serializers import (
    StudentSerializer, SignUpSerializer, SignInSerializer, ChangePasswordSerializer)
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from user.models import Student
from app.models import Checkout
from rest_framework.views import APIView
from user.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from user.tasks import send_email_registeration
from rest_framework.generics import UpdateAPIView
from django_rest_passwordreset.views import ResetPasswordConfirm


class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes=[IsAuthenticated]
    # authentication_classes=[TokenAuthentication]
    pagination_class = PageNumberPagination


class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response = {
                'message': 'logged in successfully',
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'email': user.email,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):

    def get(self, request):
        query = User.objects.all()
        serializer = SignUpSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_email_registeration.delay(request.data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, querset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'error': 'old_password is wrong'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response = {
                    'message': 'Password Change Successfully'
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    def get(self, request):
        querset = Student.objects.all()
        serializer = StudentSerializer(querset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordConfirmView(ResetPasswordConfirm):
#     def get(self,request):
#         token=request.GET.get('token')
#         response={
#             'token':token
#         }
#         return Response(response, status=status.HTTP_200_OK)
