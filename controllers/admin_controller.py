from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from extensions import db
from models.audit_log import AuditLog
from models.file import File
from models.policy import Policy
from models.user import User
from services.auth_service import admin_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "policies": Policy.query.count(),
        "files": File.query.count(),
        "audit_logs": AuditLog.query.count(),
    }

    return render_template(
        "admin_dashboard.html",
        user=current_user,
        stats=stats,
    )


@admin_bp.route("/admin/users")
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin_users.html", users=users)


@admin_bp.route("/admin/users/<int:user_id>/toggle-role", methods=["POST"])
@login_required
@admin_required
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot change your own role.")
        return redirect(url_for("admin.admin_users"))

    user.role = "ADMIN" if (user.role or "").lower() != "admin" else "user"
    db.session.commit()

    flash(f"Role updated for {user.username}.")
    return redirect(url_for("admin.admin_users"))


@admin_bp.route("/admin/policies")
@login_required
@admin_required
def admin_policies():
    policies = Policy.query.order_by(Policy.classification.asc()).all()
    return render_template("admin_policies.html", policies=policies)


@admin_bp.route("/admin/policies/new", methods=["POST"])
@login_required
@admin_required
def create_policy():
    classification = request.form.get("classification", "").strip()
    allowed_region = request.form.get("allowed_region", "").strip()
    encryption_required = request.form.get("encryption_required") == "on"

    if not classification or not allowed_region:
        flash("Classification and allowed region are required.")
        return redirect(url_for("admin.admin_policies"))

    if Policy.query.filter_by(classification=classification).first():
        flash("A policy for this classification already exists.")
        return redirect(url_for("admin.admin_policies"))

    policy = Policy(
        classification=classification,
        allowed_region=allowed_region,
        encryption_required=encryption_required,
    )

    db.session.add(policy)
    db.session.commit()

    flash("Policy added successfully.")
    return redirect(url_for("admin.admin_policies"))


@admin_bp.route("/admin/policies/<int:policy_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_policy(policy_id):
    policy = Policy.query.get_or_404(policy_id)

    db.session.delete(policy)
    db.session.commit()

    flash("Policy deleted successfully.")
    return redirect(url_for("admin.admin_policies"))
