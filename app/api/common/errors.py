"""
app.api.v1.common.errors
~~~~~~~~~~~~~~~~~~~~~~~~~

Custom error messages
"""

from flask import jsonify
from app import jwt

def raise_error(status_code, message):
    """
    Return a custom error message
    """
    response = jsonify({"status": status_code,
                        "error": message})
    response.status_code = status_code

    return response

@jwt.invalid_token_loader
def invalid_token_callback(error_msg):
    """
    Returns a custom 422 error message when a user
    provides an invalid token.

    error: Bad authorization header
    """
    return raise_error(422, "Bad authorization header")

@jwt.unauthorized_loader
def unauthorized_callback(error_msg):
    """
    Called when invalid credentials are provided.
	
	error: Unauthorized
    """
    return raise_error(401, 'Unauthorized')

@jwt.expired_token_loader
def expired_token_callback():
    """
    Returns a custom error message when a user provides
    an expired token
    """
    return raise_error(401, "Token has expired")

@jwt.revoked_token_loader
def revoked_token_callback():
    """
    Returns a custom error message when a user provides
    an expired token
    """
    return raise_error(401, "Token has been revoked")

