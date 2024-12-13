from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from utils.utils import generate_otp , send_otp_email
from django.core.cache import cache

def get_tokens_for_user(user):
    '''
    this function creates and return an object with access and refresh token.
    '''
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserSignUpView(APIView):
    """
    Validate sign up email given and send otp to email for MFA.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                role = serializer.validated_data['role']
                if role == 'admin':
                    return Response({"error": "No permission for Admin role."}, status=status.HTTP_400_BAD_REQUEST)
                email = serializer.validated_data['email']
                otp = generate_otp()

                # Store OTP in Redis cache with a 2-minute timeout
                cache.set(f"otp_{email}", otp, timeout=120)
                print('generated_otp:',otp)


                username = email.split('@')[0]
                try:
                    send_otp_email(email, username, otp)
                    return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
                except Exception as e:
                    cache.delete(f"otp_{email}")
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error:',e)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserOTPVerifyView(APIView):

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        try:
            if serializer.is_valid():

                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                role = serializer.validated_data['role']

                user = CustomUser.objects.create_user(email=email, password=password, role=role)

                if user:
                    cache.delete(f"otp_{email}")
                else:
                    return Response(
                    {"error": "User not created."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
                tokens = get_tokens_for_user(user)    
                user_serializer = UserSerializer(user)

                response = Response({
                    "message": "User created successfully.",
                    "user": user_serializer.data,
                    "access":tokens['access'],
                    "refresh":tokens['refresh'],
                }, status=status.HTTP_201_CREATED)

                return response
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print('error:', e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
     