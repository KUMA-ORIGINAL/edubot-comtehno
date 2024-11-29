from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import User


def create_user(
    telegram_id: int,
    first_name: str,
    last_name: str,
    email: str,
    role: str,
    session: Session
):
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=role
    )
    session.add(user)
    session.commit()
    return user


def get_user_by_id(telegram_id: int, session: Session):
    query = select(User).filter_by(telegram_id=telegram_id)
    user = session.execute(query)
    return user.scalar_one_or_none()

