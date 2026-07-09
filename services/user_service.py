from models import db
from models.user import User


def create_user(
    full_name,
    username,
    password,
    role
):

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:

        existing_user.full_name = full_name
        existing_user.role = role
        existing_user.active = True

        db.session.commit()

        return existing_user

    user = User(
        full_name=full_name,
        username=username,
        role=role,
        active=True,
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user