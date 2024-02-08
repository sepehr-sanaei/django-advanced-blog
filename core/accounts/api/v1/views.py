from rest_framework import generics
from .serializers import RegistrationSerializer, CustomTokenSerializer, ChangePasswordSerializer, ProfileApiSerializer, ActivationResendApiSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
from ...models import Profiles
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError , InvalidSignatureError 
from django.conf import settings
# import necessary libraries here

class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email': email,
            }
            user_obj = get_object_or_404(User, email = email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[email])
            # TODO: Add more useful commands here.
            email_obj.send()

    
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CustomDiscardToken(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ChangePasswordVIew(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
        
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old password" : "incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
            # set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"password" : "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileApiSerializer
    queryset = Profiles.objects.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
    
class TestEmail(generics.GenericAPIView):
    def get(self,request, *args, **kwargs):
        self.email = "test@test.com"
        user_obj = get_object_or_404(User, email = self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@admin.com', to=[self.email])
        # TODO: Add more useful commands here.
        email_obj.send()
        return Response("Email sent successfully")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ActivationApiToken(APIView):
    def get(self, request,token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError :
            return Response({"detail" : "Your token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"detail" : "Your token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk = user_id)
        if user_obj.is_verified:
            return Response({"detail" : "Your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail" : "Your account has been activated"})
        
    
class ActivationResendApiToken(generics.GenericAPIView):
    serializer_class = ActivationResendApiSerializer
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[user_obj.email])
        # TODO: Add more useful commands here.
        email_obj.send()
        return Response("Email sent successfully", status=status.HTTP_200_OK)

        
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)