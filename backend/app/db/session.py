import oracledb
import logging

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\Administrator\Downloads\instantclient-basic-windows.x64-19.30.0.0.0dbru\instantclient_19_30"
)

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# Oracle SQLAlchemy engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True,
)


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


# Base model
Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def create_sequences():
    """Create Oracle sequences for auto-incrementing primary keys."""
    logger = logging.getLogger(__name__)

    sequences = [
        ("users_id_seq", "CREATE SEQUENCE users_id_seq START WITH 1 INCREMENT BY 1"),
        ("orders_id_seq", "CREATE SEQUENCE orders_id_seq START WITH 1 INCREMENT BY 1"),
        ("order_status_events_id_seq", "CREATE SEQUENCE order_status_events_id_seq START WITH 1 INCREMENT BY 1"),
    ]

    with engine.connect() as conn:
        for name, ddl in sequences:
            # Oracle stores sequence names in uppercase in USER_SEQUENCES
            try:
                logger.debug(f"Checking existence of sequence {name}")
                res = conn.execute(
                    text("SELECT COUNT(*) FROM user_sequences WHERE sequence_name = :name"),
                    {"name": name.upper()},
                )
                count = res.scalar() or 0

                if count == 0:
                    logger.info(f"Creating sequence {name} with SQL: {ddl}")
                    conn.execute(text(ddl))
                    conn.commit()
                else:
                    logger.debug(f"Sequence {name} already exists")

            except Exception as exc:
                logger.error(f"Failed checking/creating sequence {name}: {exc}")
                logger.debug(f"SQL attempted: {ddl}")
                # Re-raise so startup can surface the issue (main startup logs exceptions)
                raise


def promote_user_to_admin(user_id: int):
    """Promote a user to ADMIN role for testing purposes."""
    logger = logging.getLogger(__name__)

    with engine.connect() as conn:
        try:
            logger.info(f"Promoting user {user_id} to ADMIN role.")
            conn.execute(
                text("UPDATE users SET role = 'ADMIN' WHERE id = :user_id"),
                {"user_id": user_id},
            )
            conn.commit()
            logger.info(f"User {user_id} successfully promoted to ADMIN.")
        except Exception as exc:
            logger.error(f"Failed to promote user {user_id} to ADMIN: {exc}")
            raise
