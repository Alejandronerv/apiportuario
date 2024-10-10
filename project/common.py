# Import necessary modules and classes
from datetime import timedelta  # Import timedelta for time-based operations
import jwt  # Import jwt for JSON Web Token encoding and decoding
from datetime import datetime  # Import datetime for date and time operations
from fastapi.security import OAuth2PasswordBearer  # Import OAuth2PasswordBearer for token-based authentication
from fastapi import Depends  # Import Depends for dependency injection

# Define the secret key used for JWT encoding and decoding
SECRET_KEY = 'a545701d8746a30df861027c05d3d443a3e90853e6b233411c6780e885fe2ec695d702de29eb4efe35fbead2bc58f603b3cddc932ea0ccf42224a0587c4cd1d91f3fbedf3015e9576420b16991ea69665ce3a664f77f1b930e8e3e4babedd9fd9b4fdeceed8b76eef182e936b58537e94eb1316d0daee882a21c291b0c351acba20fddf098ba9ac5ec2cc34a9b052124d1780c9a59fee2cf5887e319b4faa5ac8b1642a15fc9d40eeee26a4cec5ba6b356319fba8b25b0ce8a01cfb70c694039557812d3cd4cc25a58c60ac21b3cd45234ed6fc11ee21bf5d25959519676ab3dce5da3d7d50b07dcf7481a2c533d80dbee855b55f055df5304df9832e405fe73'

# Define the OAuth2PasswordBearer instance for token URL
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth')

# Function to create an access token
def create_access_token(user, days=7):
    # Define the payload data for the JWT
    data = {
        'user_name': user,  # Include the user name in the token
        'exp': datetime.utcnow() + timedelta(days=days)  # Set the expiration time for the token
    }

    # Encode the data using the secret key and HS256 algorithm
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")
