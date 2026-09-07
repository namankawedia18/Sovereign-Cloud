import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from services.encryption_service import (
    encrypt_file,
    decrypt_file
)
from io import BytesIO
from services.storage_service import save_file
from services.auth_service import admin_required
from flask_login import login_required, current_user
from services.audit_service import log_action
from werkzeug.utils import secure_filename
from flask import send_file
from extensions import db
from models.file import File
from services.policy_service import get_policy
from models.audit_log import AuditLog


file_bp = Blueprint("file", __name__)

UPLOAD_FOLDER = "uploads"


@file_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        uploaded_file = request.files.get("file")
        classification = request.form.get("classification")

        if not uploaded_file:
            flash("Please select a file.")
            return redirect(url_for("file.upload"))

        if not classification:
            flash("Please select a classification.")
            return redirect(url_for("file.upload"))

        # Get policy for selected classification
        policy = get_policy(classification)

        if not policy:
            flash("No policy exists for this classification.")
            return redirect(url_for("file.upload"))

        # Get the region from the policy
        storage_region = policy.allowed_region

        # Create region directory
        region_folder = os.path.join(
            UPLOAD_FOLDER,
            storage_region
        )

        os.makedirs(
            region_folder,
            exist_ok=True
        )

        # Secure the filename
        filename = secure_filename(
            uploaded_file.filename
        )

        # Storage path
        storage_path = os.path.join(
            region_folder,
            filename
        )

        if policy.encryption_required:

            encrypted_filename = filename + ".encrypted"

            encrypted_path = os.path.join(
                region_folder,
                encrypted_filename
            )

            temporary_path = os.path.join(
                region_folder,
                "temp_" + filename
            )

            save_file(
                uploaded_file,
                temporary_path
            )

            encrypt_file(
                temporary_path,
                encrypted_path
            )

            os.remove(temporary_path)

            storage_path = encrypted_path

        else:

            save_file(
                uploaded_file,
                storage_path
            )

        # Save metadata in PostgreSQL
        new_file = File(
            filename=filename,
            storage_key=storage_path,
            classification=classification,
            storage_region=storage_region,
            owner_id=current_user.id
        )

        db.session.add(new_file)
        db.session.commit()

        log_action(
            user_id=current_user.id,
            action="UPLOAD",
            file_id=new_file.id,
            filename=new_file.filename,
            classification=new_file.classification,
            storage_region=new_file.storage_region
        )

        flash(
            f"File uploaded successfully to {storage_region} region."
        )

        return redirect(
            url_for("file.upload")
        )

    return render_template("upload.html")

@file_bp.route("/files")
@login_required
def files():

    user_files = File.query.filter_by(
        owner_id=current_user.id
    ).all()

    return render_template(
        "files.html",
        files=user_files
    )

@file_bp.route("/download/<int:file_id>")
@login_required
def download(file_id):

    file = File.query.get_or_404(file_id)

    # Check ownership
    if file.owner_id != current_user.id:
        flash("You are not authorized to download this file.")
        return redirect(url_for("file.files"))

    # Record download
    log_action(
        user_id=current_user.id,
        action="DOWNLOAD",
        file_id=file.id,
        filename=file.filename,
        classification=file.classification,
        storage_region=file.storage_region
    )

    # If encryption is required, decrypt the file
    policy = get_policy(file.classification)

    if policy and policy.encryption_required:

        decrypted_data = decrypt_file(
            file.storage_key
        )

        return send_file(
            BytesIO(decrypted_data),
            as_attachment=True,
            download_name=file.filename
        )

    # Normal file
    return send_file(
        file.storage_key,
        as_attachment=True,
        download_name=file.filename
    )

@file_bp.route("/audit-logs")
@login_required
@admin_required
def audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).all()

    print("LOG COUNT =", len(logs))

    for log in logs:
        print(log.action, log.filename)

    return render_template(
        "audit_logs.html",
        logs=logs
    )