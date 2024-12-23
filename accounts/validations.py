import re
from rest_framework import serializers
from rest_framework.serializers import ValidationError # type: ignore
import dns.resolver # type: ignore
import phonenumbers # type: ignore

def validate_password(password, password2):

    """
    Validates the password and raises ValidationError if invalid.
    """
    if password != password2:
        raise serializers.ValidationError("Passwords do not match.")

    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")

    if not re.search(r'[A-Z]', password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise serializers.ValidationError("Password must contain at least one special character.")

    if re.search(r'\s', password):
        raise serializers.ValidationError("Password cannot contain spaces.")


def validate_email(email):
    """
        Validates the email format and dmain

    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise serializers.ValidationError("Invalid email format.")
    try:
        local_part, email_domain = email.split('@')
    except ValueError:
        raise ValidationError("Invalid email format. Missing '@'.")

    # Validate the local part
    if len(local_part) < 3:
        raise ValidationError("The email part before '@' must be at least 3 characters long.")
    
    if not re.fullmatch(r'[a-zA-Z0-9._]+', local_part):
        raise ValidationError("The email part before '@' contains invalid characters. Only letters, digits, dots (.), and underscores (_) are allowed.")


    try:
        # Query MX records for the domain
        dns.resolver.resolve(email_domain, 'MX')
    except dns.resolver.NoAnswer:
        raise ValidationError(f"The domain {email_domain} does not have valid email servers.")
    except dns.resolver.NXDOMAIN:
        raise ValidationError(f"The domain {email_domain} does not exist.")
def validate_first_last_name(first_name, last_name):
    if not first_name or not last_name:
        raise serializers.ValidationError(
            {"first_name_last_name": "First name and last name are required."}
        )
    if not first_name.isalpha() or not last_name.isalpha():
        raise serializers.ValidationError(
            {"first_name_last_name": "First name and last name must contain only alphabetic characters."}
        )
    if len(first_name) < 2 or len(last_name) < 2:
        raise serializers.ValidationError(
            {"first_name_last_name": "First name and last name must be at least 2 characters long."}
        )

def validate_phone_number(value):
    """
    Validates the phone number format.
    If the input is a PhoneNumber object, extracts its raw value for validation.
    """
    if value in [None, ""]:
        return

    # If value is a PhoneNumber object, extract the raw input
    if hasattr(value, 'raw_input'):
        value = value.raw_input
    #try:
        # Parse the phone number
    phone = phonenumbers.parse(value, None)  # None means no default region
    if not phonenumbers.is_valid_number(phone):
        raise ValidationError("Invalid phone number.")
    #except phonenumbers.NumberParseException:
    #   raise ValidationError("Invalid phone number format.")
    


