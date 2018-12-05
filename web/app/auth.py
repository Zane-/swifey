import ast
import requests

def is_valid_auth(cookie):
    """Returns whether or not an auth cookie is valid.
    The cookie is valid if it is less than a week old and the
    user id matches the authenticator object in the Authenticator table."""
    auth = cookie.get('auth')
    if not auth:
        return False
    # takes the string representing the dict and converts it to a dict
    auth = ast.literal_eval(auth)
    req = requests.post('http://exp-api:8000/api/validate_auth/', data=auth)
    if req.status_code == 200:
        return True
    else:
        return False
