from models.policy import Policy


def get_policy(classification):

    return Policy.query.filter_by(
        classification=classification
    ).first()