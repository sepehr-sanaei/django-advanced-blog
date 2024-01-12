from rest_framework import generics
from .serializers import RegistrationSerializer, CustomTokenSerializer, ChangePasswordSerializer, ProfileApiSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from accounts.models import User
from ...models import Profiles
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
# import necessary libraries here

class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email':serializer.validated_data['email']
            }
            
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        send_mail(
            "test email",
            "This is a test email to check the terminal email",
            "sepehr.sae.81@gmail.com",
            ["sepehr.sanaie.81@gmail.com"],
            fail_silently=False,
        )
        return Response("Email sent successfully")

        