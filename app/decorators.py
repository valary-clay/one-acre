"""

app.decorators
~~~~~~~~~~~~~~

Custom decorators

"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models import User

def admin_required(fn):
    """
    Checks user is admin status is True before allowing access
    to endpoint
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()
        if not user.admin:
            return {'status': 403, 'message': 'Only admins can access this endpoint'}, 403
        return fn(*args, **kwargs)
    return wrapper


