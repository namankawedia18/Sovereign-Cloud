from extensions import db


class Policy(db.Model):
    __tablename__ = "policies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    classification = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    allowed_region = db.Column(
        db.String(100),
        nullable=False
    )

    encryption_required = db.Column(
        db.Boolean,
        default=False
    )