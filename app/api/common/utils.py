"""
app.api.v1.common.utils
~~~~~~~~~~~~~~~~~~~~~~~~

some common utility functions
"""
import re
import string
import datetime
from flask import jsonify
from app import jwt
from app.helpers import is_token_revoked
from app.models import User

EMAIL_PATTERN = re.compile(r".+@[\w]+\.[\w]")

def valid_role(role):
    try:
        role = int(role)
        assert role in (0, 1)
    except (AssertionError, ValueError):
        role = None
    return role

def valid_string(value):
    if value:
        return value.strip()
    return None

def valid_farm_name(name):
    return valid_string(name)

def valid_location(location):
    return valid_string(location)

def valid_description(description):
    return valid_string(description)

def valid_date(date):
    try:
        date = datetime.datetime(*[int(x) for x in date.split('-')])
    except Exception:
        date = None
    return date

def valid_margin(margin):
    try:
        margin = float(margin)
        assert margin >= 0
        assert margin <= 100
    except (ValueError, TypeError, AssertionError):
        margin = None
    return margin

def valid_status(status):
    try:
        assert status in ('inactive', 'pending', 'confirmed')
    except AssertionError:
        status = None 
    return status

def valid_price(price):
    try:
        price = float(price)
        assert price > 0
    except (ValueError, TypeError, AssertionError):
        price = None
    return price

def valid_farm_stage(value):
    if value in ('open', 'closed'):
        return value.strip()

def valid_active_status(value):
    if value == 'active':
        return True
    return 'inactive'


def valid_email(email):
    if EMAIL_PATTERN.match(email):
        return email

def valid_units(units):
    try:
        units = int(units)
    except Exception:
        units = None
    return units

def valid_password(password):
    special_char_present = False
    for char in password:
        if char in string.punctuation:
            special_char_present = special_char_present or True
    digit_present = False
    for char in password:
        digit_present = digit_present or char.isdigit()

    if special_char_present and digit_present:
        if len(password) >= 5:
            return True

# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)

@jwt.user_loader_callback_loader
def load_user(identity):
    user = User.query.filter_by(email=identity).first()
    return user
