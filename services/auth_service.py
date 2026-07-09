from flask_login import current_user


def is_admin():

    return (
        current_user.is_authenticated
        and current_user.role == "ADMIN"
    )
def is_invoicer():

    return (
        current_user.is_authenticated
        and current_user.role == "INVOICER"
    )
from functools import wraps
from flask import abort


def admin_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if not is_admin():
            abort(403)

        return view(*args, **kwargs)

    return wrapped_view        