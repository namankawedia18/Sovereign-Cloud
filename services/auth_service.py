from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.role != "admin":
            flash("Admin access required.")
            return redirect(url_for("home"))

        return f(*args, **kwargs)

    return decorated_function