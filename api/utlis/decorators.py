from functools import wraps
from flask import abort
from ..models.user import UserModel
from flask_jwt_extended import get_jwt_identity


def permission_required():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            print("Identity:", get_jwt_identity())
            user = UserModel.query.filter_by(id=get_jwt_identity()).first()
            if not user or not user.admin:
                abort(403, "User doesn't have permissions to access this resource")
            # if not user.admin:
            #     abort(403, "User doesn't have permissions to access this resource")
            return func(*args, **kwargs)
        return decorated_function
    return decorator
