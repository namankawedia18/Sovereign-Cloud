from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            flash("Please log in first.")
            return redirect(url_for("auth.login"))

        role = current_user.role or ""

        if role.lower() != "admin":
            flash("Admin access required.")
            return redirect(url_for("auth.dashboard"))

        return f(*args, **kwargs)

    return decorated_function