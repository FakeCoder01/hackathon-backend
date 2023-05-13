from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import RegisterSerializer, OTPVerificationSerializer
from .models import Profile, Account
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import random
from rest_framework.authtoken.models import Token
# Create your views here.




class UserAccountViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return User.objects.get(user=self.request.user)

    def user_details(self, request, id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = User.objects.filter(user=self.request.user)
        user = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup_new_user(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        if request.data.get('password') == request.data.get('confirm_password'):
            user = User.objects.create_user(
                serializer.init_data['email'], # username
                serializer.init_data['email'],  # email
                serializer.init_data['password']
            )
            acc = Account.objects.create(
                user = user,
                email = serializer.init_data['email'],
            )
            otp = random.randint(1000, 9999)
            print("OTP : ", otp)
            if acc.set_otp(otp):
                acc.save()
                return Response({
                    "detail" : "otp-sent",
                    "userid" : str(user.id),
                    "next" : "verify"
                }, status=201)
            else:
                return Response({
                    "detail" : "otp couldn't set"
                }, status=500)
        return Response({
            "detail" : "password mismatch"
        }, status=402)
    return Response({"detail" : "All fields are neccessary"}, status=413)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def otp_verification(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        userid = request.data.get('userid')
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not User.objects.filter(email=email, id=userid).exists():
            return Response({"detail" : "no users with this email"}, status=404)
        user = User.objects.get(id=userid, email=email)
        if not Account.objects.filter(email=email, user=user, status=False).exists():
            return Response({"detail" : "no account with for this user"}, status=404)
        
        acc = Account.objects.get(email=email, user=user, status=False)
        if acc.verify_otp(str(otp)):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'detail' : 'verification successful', 'token' : token.key, "next" : "profile"}, status=200)
        
        return Response({'detail' : 'wrong otp'}, status=400)
    return Response(serializer.errors, status=400)
