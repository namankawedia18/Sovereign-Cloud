from extensions import db
from models.audit_log import AuditLog


def log_action(
    user_id,
    action,
    file_id=None,
    filename=None,
    classification=None,
    storage_region=None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        file_id=file_id,
        filename=filename,
        classification=classification,
        storage_region=storage_region
    )

    db.session.add(audit_log)
    db.session.commit()