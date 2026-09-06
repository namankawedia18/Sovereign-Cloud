from app import app
from extensions import db
from models.policy import Policy


with app.app_context():

    policies = [

        Policy(
            classification="Government",
            allowed_region="Mumbai",
            encryption_required=True
        ),

        Policy(
            classification="Healthcare",
            allowed_region="Delhi",
            encryption_required=True
        ),

        Policy(
            classification="Public",
            allowed_region="Bangalore",
            encryption_required=False
        )
    ]

    for policy in policies:

        existing = Policy.query.filter_by(
            classification=policy.classification
        ).first()

        if not existing:
            db.session.add(policy)

    db.session.commit()

    print("Policies inserted successfully")