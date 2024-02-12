from base64 import urlsafe_b64decode
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, serializers, status, views
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from ciso_assistant.settings import EMAIL_HOST, EMAIL_HOST_RESCUE

from .serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    SetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)

from .models import Role, RoleAssignment

User = get_user_model()


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None) -> Response:
        serializer = LoginSerializer(
            data=self.request.data,  # type: ignore
            context={"request": self.request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        login(request, user)
        return Response(None, status=HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    @method_decorator(ensure_csrf_cookie)
    def post(self, request) -> Response:
        logout(request)
        return Response({"message": "Logged out successfully."}, status=HTTP_200_OK)


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                {"error": "You are not logged in. Please ensure you are logged in."},
                status=HTTP_401_UNAUTHORIZED,
            )
        res_data = {
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "is_active": request.user.is_active,
            "date_joined": request.user.date_joined,
            "user_groups": request.user.get_user_groups(),
            "permissions": request.user.permissions,
        }
        return Response(res_data, status=HTTP_200_OK)


class PasswordResetView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        email = request.data["email"]  # type: ignore
        associated_users = User.objects.filter(email=email)
        if EMAIL_HOST or EMAIL_HOST_RESCUE:
            if associated_users and associated_users.exists():
                associated_user = associated_users[0]
                try:
                    associated_user.mailing(
                        email_template_name="registration/password_reset_email.html",
                        subject=_("Ciso: Password Reset"),
                    )
                    print("Sending reset mail to", email)
                except Exception as e:
                    print(e)
            return Response(status=HTTP_202_ACCEPTED)
        return Response(
            data={
                "error": "Email server not configured, please contact your administrator"
            },
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
class ResetPasswordConfirmView(views.APIView):
    """
    API Endpoit for reset password confirm
    """
    default_token_generator = PasswordResetTokenGenerator()
    permission_classes = [permissions.AllowAny]
    serialier_class = ResetPasswordConfirmSerializer
    token_generator = default_token_generator

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_b64decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
        ):
            user = None
        return user

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data.get("uidb64")
        token = serializer.validated_data.get("token")
        new_password = serializer.validated_data.get("new_password")
        user = self.get_user(uidb64)
        if user is not None:
            if self.token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
        return Response(
                    data={"error": "The link is invalid or has expired."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

class ChangePasswordView(views.APIView):
    """
    An endpoint for changing password.
    """

    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                "Your old password was entered incorrectly. Please enter it again."
            )
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class SetPasswordView(views.APIView):
    """
    An endpoint for setting a password as an administrator.
    """

    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = SetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if RoleAssignment.has_role(
            self.request.user, Role.objects.get(name="BI-RL-ADM")
        ):
            new_password = serializer.validated_data.get("new_password")
            user = serializer.validated_data.get("user")
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
