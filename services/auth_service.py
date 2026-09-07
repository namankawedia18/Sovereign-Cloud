from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Check if user is logged in
        if not current_user.is_authenticated:
            print("NOT AUTHENTICATED")
            flash("Please log in first.")
            return redirect(url_for("login"))

        print("ROLE =", current_user.role)

        # Check admin role
        if current_user.role.lower() != "admin":
            print("DENIED")
            flash("Admin access required.")
            return redirect(url_for("home"))

        print("GRANTED")
        return f(*args, **kwargs)

    return decorated_function