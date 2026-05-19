from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create(
        self,
        email: str,
        hashed_password: str,
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(user)

        # IMPORTANT:
        # repositories should NOT commit
        self.db.flush()
        self.db.refresh(user)

        return user
