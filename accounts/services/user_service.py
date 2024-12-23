'''
from django.contrib.auth import get_user_model



def create_user(validated_data, user_model):
    # Pop out fields that are not required
    validated_data.pop('password2', None)  # Remove password2 as it's not needed

    # Extract relevant fields
    email = validated_data.get('email')
    first_name = validated_data.get('first_name', '')
    last_name = validated_data.get('last_name', '')
    password = validated_data.get('password')
    role = validated_data.get('role')

    # Automatically generate username from the email (before '@')
    username = email.split('@')[0]  # Extracts the part before '@'

    # Create the user object using the user_model's create_user method
    return user_model.objects.create_user(
        email=email,
        username=username,  # Set username here explicitly
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=role
    )
    '''