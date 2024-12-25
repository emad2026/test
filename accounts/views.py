from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Client, OneTimePassword, Captain
from accounts.serializers import ClientLoginSerializer, ClientRegistrationSerializer, ClientResendOTPSerializer, ClientResetPasswordSerializer, CaptainLoginSerializer, CaptainRegistrationSerializer, CaptainResendOTPSerializer, CaptainResetPasswordSerializer
#from accounts.services.profile_service import create_driver_profile, create_passenger_profile
from rest_framework.views import APIView
from accounts.utils import  send_otp_for_captain, send_otp_for_client, send_otp_for_password_reset, send_otp_for_password_reset, send_otp_for_captain, send_verification_email
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
SECRET_KEY = settings.SECRET_KEY
from accounts.validations import validate_password
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from datetime import timedelta
#from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
#from accounts.services.user_service import create_user
from django.contrib.auth.hashers import check_password
#User = get_user_model()
#logger = logging.getLogger(__name__)




#Registration
class CaptainRegisterView(APIView):
    def post(self, request):
        #logger.info(f"Received request data: {request.data}")
        serializer = CaptainRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            captain = serializer.save()
            #logger.info(f"Captain created: {captain.email}")

            # Step 2: Send OTP to the captain's email using the utility function
            #                                                                                           
            send_otp_for_captain(captain.email)
            
                #logger.info(f"OTP sent to {captain.email}")
            #except Exception as e:
                #logger.error(f"Error sending OTP: {str(e)}")
            
            # Step 3: Return success response
            return Response({
                'message': 'Captain registered successfully',
                'data': {
                    'email': captain.email
                }
            }, status=status.HTTP_201_CREATED)
        


        
        # Log the errors in case of invalid serializer
        #logger.error(f"Serializer validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientRegisterView(APIView):
    def post(self, request):
        #logger.info(f"Received request data: {request.data}")
        serializer = ClientRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            client = serializer.save()   
            #logger.info(f"Client created: {client.email}")

            # Step 2: Send OTP to the client's email using the utility function
            #try:
            send_otp_for_client(client.email)
                #logger.info(f"OTP sent to {client.email}")
            #except Exception as e:
                #logger.error(f"Error sending OTP: {str(e)}")
            
            # Step 3: Return success response
            return Response({
                'message': 'Client registered successfully',
                'data': {
                    'email': client.email
                }
            }, status=status.HTTP_201_CREATED)
        
        # Log the errors in case of invalid serializer
        #logger.error(f"Serializer validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get('otp_code')

        # Ensure OTP code is provided
        if not otp_code:
            return Response({
                'message': 'OTP code is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the OTP record from OneTimePassword model
            otp = OneTimePassword.objects.get(otp=otp_code)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Invalid OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check OTP expiration
        if otp.is_expired():
            #otp.delete()
            return Response({
                'message': 'OTP has expired'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Determine if the OTP belongs to a Captain or Client
        if otp.captain:
            user = otp.captain
        elif otp.client:
            user = otp.client
        else:
            return Response({
                'message': 'No associated user for this OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is already verified
        if user.is_verified:
            return Response({
                'message': 'Email already verified',
                'data': {
                    'email': user.email,
                    'is_verified': user.is_verified
                }
            }, status=status.HTTP_200_OK)

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Send verification success email
        send_verification_email(user, otp_code)  # Assuming this sends the confirmation email

        # Optionally delete OTP record after successful verification
        otp.delete()

        return Response({
            'message': 'Email verified successfully',
            'data': {
                'email': user.email,
                'is_verified': user.is_verified
            }
        }, status=status.HTTP_200_OK)


#Resend OTP
class CaptainResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CaptainResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = Captain.objects.get(email=email)

            if user.is_verified:
                return Response(
                    {'message': 'Your account has already been verified. Please go to the login page.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            send_otp_for_captain(user.email)
        except Captain.DoesNotExist:
            return Response({'message': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'OTP has been resent to your email.'}, status=status.HTTP_200_OK)

class ClientResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientResendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        try:
            user = Client.objects.get(email=email)
            if user.is_verified:
                return Response(
                    {'message': 'Your account has already been verified. Please go to the login page.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            send_otp_for_client(user.email)
        except Client.DoesNotExist:
            return Response({'message': 'No user found with this email.'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({'message': 'OTP has been resent to your email.'}, status=status.HTTP_200_OK)


#Reset password Captain
class CaptainPasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            captain = Captain.objects.get(email=email)
        except Captain.DoesNotExist:
            return Response({'message': 'Captain with this email does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)
        

        # Send OTP for password reset
        try:
            send_otp_for_password_reset(email, user_type='captain')
            return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CaptainResetPasswordView(APIView):
    """
    This view allows a captain to reset their password after OTP verification.
    """
    def post(self, request):
        serializer = CaptainResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Reset password Client
class ClientPasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Client.objects.get(email=email)
        except Client.DoesNotExist:
            return Response({'message': 'Client with this email does not exist.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Send OTP for password reset
        try:
            send_otp_for_password_reset(email, user_type='client')
            return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ClientResetPasswordView(APIView):
    """
    This view allows a client to reset their password after OTP verification.
    """
    def post(self, request):
        serializer = ClientResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Login and genratethe JWT Tokens
class CaptainLoginView(APIView):
    def post(self, request):
        # Deserialize the captain login data
        serializer = CaptainLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            captain = serializer.validated_data  # Extract the validated captain
            if not captain.is_verified:
                return Response(
                    {'message': 'Your account is not verified. Please verify your account to proceed.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Generate refresh token and include captain_id in the token payload
            refresh = RefreshToken.for_user(captain)
            refresh['captain_id'] = captain.id  # Explicitly add captain_id to the token payload

            # Generate access token
            access_token = refresh.access_token

            # Return tokens
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientLoginView(APIView):
    def post(self, request):
        # Create the serializer with the request data
        serializer = ClientLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            
            client = serializer.validated_data
            if not client.is_verified:
                return Response(
                    {'message': 'Your account is not verified. Please verify your account to proceed.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Generate refresh token and include client_id
            refresh = RefreshToken.for_user(client)
            refresh['client_id'] = client.id

            # Generate access token
            access_token = refresh.access_token

            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#logout for both Captain and Client and set token to be expired
class CaptainLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token not provided."}, 
                    status=status.HTTP_400_BAD_REQUEST)

            # Decode the refresh token
            token = RefreshToken(refresh_token)
            captain_id_in_token = token.payload.get('captain_id')

            if not captain_id_in_token:
                return Response({"detail": "Invalid token: captain_id missing."}, status=status.HTTP_403_FORBIDDEN)

            # Validate that the captain exists and matches the current authenticated captain
            captain = Captain.objects.filter(id=captain_id_in_token).first()
            if not captain:
                return Response({"detail": "Invalid token: Captain not found."}, status=status.HTTP_403_FORBIDDEN)

            # Optionally, you could also check if the captain is the one making the request, for example:
            # if captain.id != request.user.id:  # Make sure the user is the same
            #     return Response({"detail": "Token does not belong to the authenticated captain."}, status=status.HTTP_403_FORBIDDEN)

            # Expire the token (logout the captain)
            token.set_exp()

            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ClientLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request body
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token not provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Decode the token
            token = RefreshToken(refresh_token)
            client_id_in_token = token.payload.get('client_id')

            # Validate the client exists
            
            if not client_id_in_token:
                return Response({"detail": "Invalid token: client_id missing."}, status=status.HTTP_403_FORBIDDEN)

            # Validate that the client exists and matches the current authenticated client
            client = Client.objects.filter(id=client_id_in_token).first()
            if not client:
                return Response({"detail": "Invalid token: client not found."}, status=status.HTTP_403_FORBIDDEN)
            '''
            # Optionally, ensure the token belongs to the correct user type (Client)
            if not hasattr(client, 'clientprofile'):  # Adjust based on your implementation
                return Response(
                    {"detail": "Token does not belong to a client."},
                    status=status.HTTP_403_FORBIDDEN
                )
            '''

            # Expire the token
            token.set_exp()  # This expires the token immediately

            return Response(
                {"detail": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
class CaptainChangePasswordView(APIView):
     def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            captain = payload.get('captain_id')

            # Fetch the Captain
            captain = Captain.objects.get(id=captain)

            # Validate old password
            old_password = request.data.get('old_password')
            if not old_password or not check_password(old_password, captain.password):
                raise ValidationError({"old_password": "Old password is incorrect."})
            # Validate new passwords
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            validate_password(new_password,confirm_password)
            # Change password
            captain.set_password(new_password)
            captain.save()
            return Response({"message": "Password changed successfully."}, status=200)
        except jwt.ExpiredSignatureError:
            pass
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            print("Invalid token.")
            raise AuthenticationFailed('Invalid token')
        except Captain.DoesNotExist:
            raise AuthenticationFailed('Captain not found')
                    
        except ValidationError as e:
                    return Response(e.detail, status=400)
        
class clientChangePasswordView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            client_id = payload.get('client_id')

            # Fetch the client
            client = Client.objects.get(id=client_id)

            # Validate old password
            old_password = request.data.get('old_password')
            if not old_password or not check_password(old_password, client.password):
                raise ValidationError({"old_password": "Old password is incorrect."})

            # Validate new passwords
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            validate_password(new_password, confirm_password)

            # Change password
            client.set_password(new_password)
            client.save()

            return Response({"message": "Password changed successfully."}, status=200)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Client.DoesNotExist:
            raise AuthenticationFailed('Client not found')
        except ValidationError as e:
            return Response(e.detail, status=400)
        