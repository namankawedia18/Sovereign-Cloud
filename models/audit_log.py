from extensions import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(50),
        nullable=False
    )

    file_id = db.Column(
        db.Integer,
        db.ForeignKey("files.id"),
        nullable=True
    )

    filename = db.Column(
        db.String(255),
        nullable=True
    )

    classification = db.Column(
        db.String(100),
        nullable=True
    )

    storage_region = db.Column(
        db.String(100),
        nullable=True
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref("audit_logs", lazy=True)
    )

    file = db.relationship(
        "File",
        backref=db.backref("audit_logs", lazy=True)
    )