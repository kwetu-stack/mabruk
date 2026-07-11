from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from models.user import User
from models import db


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
    url_for("dashboard.home")
)

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )
# ----------------------------
# CHANGE PASSWORD
# ----------------------------
@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check current password
        if not current_user.check_password(current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))

        # Confirm passwords match
        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect(url_for("auth.change_password"))

        # Update password
        current_user.set_password(new_password)

        db.session.commit()

        flash("Password changed successfully.", "success")

        return redirect(url_for("dashboard.home"))

    return render_template(
        "users/change_password.html"
    )    