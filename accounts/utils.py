import random
from django.core.mail import send_mail
from django.template.loader import render_to_string # type: ignore
from django.utils.html import strip_tags # type: ignore
from django.conf import settings # type: ignore
from accounts.models import Client, OneTimePassword, Captain
import logging
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

logger = logging.getLogger(__name__)

def generate_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit OTP

def send_otp_for_captain(email):
    try:
        captain = Captain.objects.get(email=email)
        otp = generate_otp()

        # Create OTP record for the captain
        otp_record = OneTimePassword.objects.create(captain=captain, otp=otp)

        # Send OTP to captain's email
        context = {'name': captain.get_full_name(), 'OTP': otp}
        subject = "Captain Confirmation Email"
        template = 'index.html'
        html_content = render_to_string(template, context)
        plain_message = strip_tags(html_content)

        send_mail(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            [captain.email],
            html_message=html_content,
            fail_silently=False
        )

        logger.info(f"OTP sent to captain {captain.email}. OTP: {otp}")

    except Captain.DoesNotExist:
        logger.error(f"Captain with email {email} not found.")
        raise ValueError(f"Captain with email {email} does not exist")
    except Exception as e:
        logger.error(f"Error sending OTP to captain {email}: {str(e)}")
        raise

def send_otp_for_client(email):
    try:
        # Find the Client by email
        client = Client.objects.get(email=email)
        
        # Generate OTP
        otp = generate_otp()
        
        # Create OTP record for the client
        otp_record = OneTimePassword.objects.create(client=client, otp=otp)

        # Send OTP to the Client's email
        context = {'name': client.get_full_name(), 'OTP': otp}
        subject = "Client Confirmation Email"
        template = 'index.html'  # Update this with the appropriate template for clients
        html_content = render_to_string(template, context)
        plain_message = strip_tags(html_content)


        try:
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [client.email],
                html_message=html_content,
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            
        logger.info(f"OTP sent to client {client.email}. OTP: {otp}")

    except Client.DoesNotExist:
        logger.error(f"Client with email {email} not found.")
        raise ValueError(f"Client with email {email} does not exist")
    except Exception as e:
        logger.error(f"Error sending OTP to client {email}: {str(e)}")
        raise

def send_verification_email(user, otp):
    subject = "Email Verification - Your Account Is Confirmed"
    plain_message = f"Dear {user.first_name},\n\nPlease use the following OTP to verify your email: {otp}\n\nThank you!"
    receiver_email = user.email
    
    # Render the HTML content
    html_message = render_to_string('email_confirmation.html', {
        'name': user.first_name,
        'OTP': otp
    })
    
    # Send email
    send_mail(
        subject,
        plain_message,  # Fallback plain-text message
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[receiver_email],
        html_message=html_message,
        fail_silently=False  # Fail loudly in development
    )

def send_otp_for_password_reset(email, user_type):
    otp = generate_otp()

    if user_type == 'captain':
        try:
            user = Captain.objects.get(email=email)
        except Captain.DoesNotExist:
            raise ValueError(f"Captain with email {email} not found")
    elif user_type == 'client':
        try:
            user = Client.objects.get(email=email)
        except Client.DoesNotExist:
            raise ValueError(f"Client with email {email} not found")

    # Create OTP record
    otp_record = OneTimePassword.objects.create(
        otp=otp,
        captain=user if user_type == 'captain' else None,
        client=user if user_type == 'client' else None
    )

    # Send OTP to the user's email
    context = {'name': user.get_full_name(), 'OTP': otp}
    subject = f"{user_type.capitalize()} Password Reset OTP"
    template = 'reset_otp_email.html'  # Your email template for OTP
    html_content = render_to_string(template, context)
    plain_message = strip_tags(html_content)
    receiver_email = user.email
 

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        recipient_list=[receiver_email],
        html_message=html_content,
        fail_silently=False
    )

    #return otp_record  # Optionally return OTP for debugging/logging purposes

def send_reset_password_confirm(user):
    subject = "Reset Password Confirmation"
    plain_message = f"Dear {user.first_name}, your password has been successfully reseted "
    receiver_email = user.email
    
    # Render the HTML content
    html_message = render_to_string('password_reset_confirm.html', {
        'name': user.first_name,
    })

    # Send email
    send_mail(
        subject,
        plain_message,  # Fallback plain-text message
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[receiver_email],
        html_message=html_message,
        fail_silently=False  # Fail loudly in development
    )


'''
def verify_otp(otp_code):

        #otp_code = request.data.get('otp_code')

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

'''


