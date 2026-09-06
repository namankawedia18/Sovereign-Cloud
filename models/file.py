from extensions import db
from datetime import datetime


class File(db.Model):
    __tablename__ = "files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    storage_key = db.Column(
        db.String(500),
        nullable=False
    )

    classification = db.Column(
        db.String(100),
        nullable=False
    )

    storage_region = db.Column(
        db.String(100),
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    owner = db.relationship(
        "User",
        backref=db.backref("files", lazy=True)
    )