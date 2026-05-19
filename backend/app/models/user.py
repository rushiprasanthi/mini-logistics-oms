from sqlalchemy import Column, Integer, String, Boolean, Sequence
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        Sequence('users_id_seq'),
        primary_key=True,
        index=True,
    )
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False, server_default="user")
