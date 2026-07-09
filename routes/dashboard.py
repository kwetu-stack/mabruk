from flask import Blueprint, render_template
from flask_login import login_required

from services.auth_service import admin_required

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
)


@dashboard_bp.route("/")
@login_required
def home():

    return render_template(
        "dashboard.html"
    )
@dashboard_bp.route("/admin")
@login_required
@admin_required
def admin_panel():

    return (
        "<h2>Administrator Access Confirmed</h2>"
        "<p>Authorization layer is working.</p>"
    )    