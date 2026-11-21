from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import NotAuthenticated
from .otp import OTPService, check_limited
from .serializers import AuthenticatedSerializer, LoginOrRegisterSerializer, LogoutSerializer


# Authentication Views
class AuthenticatedView(APIView):
    """  
        Sends an OTP to a phone number for authentication.

        - Only accessible to unauthenticated users (logged-in users get 403).
        - Rate-limited to 3 requests per 60 minutes per phone number.
        - Stores only the phone number in the session for the verify step.
        - Returns: 200 (sent), 400 (invalid input), 403 (already logged in),
        429 (rate limit exceeded).
    """

    serializer_class = AuthenticatedSerializer
    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer_data = self.serializer_class(data = request.data)

        if serializer_data.is_valid():
            phone = serializer_data.validated_data["phone"]

            if not check_limited(f"user_limited_{phone}", 3, 60):
                return Response({"message":"The number of requests has reached the limit. Please try again in an hour."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            code = OTPService.send_otp_for_user(phone)
            request.session["user_info"] = {"phone":phone}
            print(code)
            return Response({"message":f"Code send to {phone}"}, status=status.HTTP_200_OK)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginOrRegisterView(APIView):
    """
        Log in or register a user via OTP code or password.

        Prerequisites:
            - The user must have previously stored their phone number in the
            session via AuthenticatedView (key: "user_info").
            - Otherwise, a 400 response ("start over from the beginning") is returned.

        Two authentication paths:
            1. OTP code (field: code):
            - If the user exists: the code is verified and, on success,
                access and refresh tokens are returned.
            - If the user does not exist: after successful verification,
                a new account is created and tokens are returned (auto-register).
            2. Password (field: password):
            - Only for existing users with a usable password.
            - On success, access and refresh tokens are returned.

        Access control:
            - Only unauthenticated users (permission_classes = [NotAuthenticated]).

        Security notes:
            - The "user_info" session key is cleared after a successful login.
            - Deactivated users (is_active=False) are rejected with 403.
            - In the password flow, the same error (403) is returned for both
            "user not found" and "wrong password" to prevent enumeration.
            - Tokens are issued via SimpleJWT (RefreshToken).

        Responses:
            - 200: successful login/registration + tokens.
            - 400: missing session, invalid code, or neither code nor password provided.
            - 403: deactivated user or invalid credentials.
    """
    serializer_class = LoginOrRegisterSerializer
    permission_classes = [NotAuthenticated]

    # helpers methods
    @staticmethod
    def _issue_tokens(user):
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "logged in successfully",
                "user": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _clear_session(request):
        request.session.pop("user_info", None)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_session = request.session.get("user_info")
        if not user_session:
            return Response(
                {"message": "This page is not available. Please start the process over from the beginning."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone = user_session.get("phone")
        code = serializer.validated_data.get("code")
        password = serializer.validated_data.get("password")

        if code:
            return self._handle_otp(request, phone, code)
        if password:
            return self._handle_password(request, phone, password)

        return Response(
            {"message": "Enter the verification code or password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def _handle_otp(self, request, phone, code):
        invalid_code = Response(
            {"message": "The entered code is incorrect or invalid."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        user = User.objects.filter(phone=phone).first()

        if user and not user.is_active:
            return Response(
                {"message": "Your account has been deactivated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not OTPService.verify_otp(phone, code):
            return invalid_code

        if user is None:
            user = User.objects.create_user(phone=phone)

        self._clear_session(request)
        return self._issue_tokens(user)

    def _handle_password(self, request, phone, password):
        user = User.objects.filter(phone=phone).first()

        no_password = Response(
            {"message": "No password has been set for this account. Sign in using a verification code."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        if user is None:
            return no_password

        if not user.is_active:
            return Response(
                {"message": "Your account has been deactivated."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not user.has_usable_password():
            return no_password

        if not authenticate(phone=phone, password=password):
            return Response(
                {"message": "The information is invalid."},
                status=status.HTTP_403_FORBIDDEN,
            )

        self._clear_session(request)
        return self._issue_tokens(user)

class LogoutView(APIView):

    """
        Log out the current user by blacklisting their refresh token.

        How it works:
            - The client sends the refresh token in the request body.
            - The token is added to the blacklist so it can no longer be used
            to obtain new access tokens.

        Access control:
            - Only authenticated users (permission_classes = [IsAuthenticated]).
            - Requires a valid access token in the Authorization header.

        Notes:
            - The access token itself is NOT invalidated here; it remains valid
            until it expires. Only the refresh token is revoked.
            - Blacklisting requires `rest_framework_simplejwt.token_blacklist`
            to be added to INSTALLED_APPS.

        Responses:
            - 200: refresh token blacklisted successfully.
            - 400: invalid input, or the token was already blacklisted / invalid.
    """

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer_data = self.serializer_class(data = request.data)
        if serializer_data.is_valid():
            try:
                refresh = serializer_data.validated_data.get("refresh_token")
                token = RefreshToken(refresh)
                token.blacklist()
                return Response({"message":"Deleted refresh_token successfuly."}, status=status.HTTP_200_OK)
            except:
                return Response({"message":"The token has already been deleted."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

# Profile views






















