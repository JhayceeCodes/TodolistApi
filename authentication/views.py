from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from core.views import BaseAPIView
from core.utils import send_mail
from .serializers import UserSerializer
from authToken.tokens import generate_access_token, decode_access_token, generate_refresh_token, decode_refresh_token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import jwt
from .models import User


class RegisterView(APIView, BaseAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email = serializer.data["email"])
        access_token = generate_access_token(user.id)
        
        current_site = get_current_site(request).domain
        relative_link = reverse("verify_email")
        absurl = "http://"+current_site+relative_link+"?token="+str(access_token)

        body = f"Hi {user.first_name}, please click the link below to verify your account \n{absurl}"
        subject = "Verify your email"
        receiver = user.email
        data = {"body": body, "subject": subject, "receiver": receiver}

        #send_mail(data)

        return self.format_response(
            message="account created, check email for verification link",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView, BaseAPIView):
    def get(self, request):
        access_token = request.GET.get("token")

        try:
            id = decode_access_token(access_token)
            user = User.objects.get(id = id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return self.format_response(message="email successfully activated")
        except jwt.ExpiredSignatureError:
            return self.format_response(
                message="activation link has expired",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST    
                )
        except jwt.exceptions.DecodeError:
            return self.format_response(
                message="invalid token",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )
            

class LoginView(APIView, BaseAPIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = User.objects.get(email=email)

            if not user.check_password(password):
                return self.format_response(
                    message="Incorrect password",
                    success=False,
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                access_token = generate_access_token(user.id)
                refresh_token = generate_refresh_token(user.id)

                response = Response()
                response.set_cookie(key="refreshToken",
                                    value=refresh_token, httponly=True)
                response.set_cookie(key="accessToken",
                                    value=access_token, httponly=True)

                response.data = {
                    "refresh": refresh_token,
                    "access": access_token
                }

                return response

        except User.DoesNotExist:
            return self.format_response(
                message="User not found",
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        

class UserView(APIView, BaseAPIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1]
            id = decode_access_token(token)
            if id is not None:
                user = User.objects.get(id=id)
                return self.format_response(
                    message="User authenticated",
                    data=UserSerializer(user).data,
                    success=True
                )
            else:
                return self.format_response(
                    message="Invalid access token",
                    success=False,
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return self.format_response(
                message="Invalid request header",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView, BaseAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie("accessToken")
        response.delete_cookie("refreshToken")
        response.data = {
            "message": "Logout successful",
            "data": "",
            "success": True
        }
        response.status = status.HTTP_204_NO_CONTENT

        return response
    

class RefreshView(APIView, BaseAPIView):
    def post(self, request):
        token = request.COOKIES.get("refreshToken")
        try:
            id = decode_refresh_token(token)
            access_token = generate_access_token(id)

            response = Response()
            response.set_cookie(key="accessToken",
                                value=access_token, httponly=True)
            response.data = {
                "access": access_token
            }

            return response

        except:
            return self.format_response(
                message="Invalid refresh token",
                success=False,
                status_code=status.HTTP_404_NOT_FOUND
            )


class RequestPasswordResetView(APIView, BaseAPIView):
    def post(self, request):
        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request).domain
            relative_link = reverse("confirm_password_reset", kwargs={"uidb64": uidb64, "token": token})
            absurl = "http://"+current_site+relative_link
            body = f"Hello, \n use the link below to reset your password \n{absurl}"
            subject = "Reset Password"
            receiver = user.email
            data = {"body": body, "subject": subject, "receiver": receiver}
            send_mail(data)

            return self.format_response(
                message="we have sent you a link to reset your password",
                status_code=status.HTTP_200_OK
            )
        
        else:
            return self.format_response(
                message="email does not exist",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )


        
    

class PasswordResetConfirmView(APIView, BaseAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
               return self.format_response(
                   message="invalid token",
                   success=False,
                   status_code=status.HTTP_401_UNAUTHORIZED
               )
            
            return self.format_response(
                message=f"credentials valid, 'uidb64':{uidb64}; 'token': {token}"
            )
        except DjangoUnicodeDecodeError:
            return self.format_response(
                message="invalid token",
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
class SetNewPasswordView(APIView, BaseAPIView):
    def patch(self, request):
        try:
            password = request.data.get("password", "")
            token = request.data.get("token", "")
            uidb64 = request.data.get("uidb64", "")

            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
               return self.format_response(
                   message="invalid reset link",
                   success=False,
                   status_code=status.HTTP_401_UNAUTHORIZED
               )
            user.set_password(password)
            user.save()
            return self.format_response(
                message="password reset successful",
            )
        except DjangoUnicodeDecodeError:
            return self.format_response(
                message="invalid rest link",
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )

