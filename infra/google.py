import requests
from rest_framework.validators import ValidationError

def verify_google_token(token):
    try:
        response = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
            "Authorization": f"Bearer {token}"
        })

        user_info = response.json()
        print(user_info)
        return user_info
    except Exception as error:
        raise ValidationError(f"Error validating token: {error}")