import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.order_event import OrderStatusEvent
from app.repositories.user_repo import UserRepository
from app.repositories.order_repo import OrderRepository
from app.services.order_service import OrderService


@pytest.fixture()
def db_session():
    engine = create_engine('sqlite:///:memory:')
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_transition_happy_path(db_session):
    user_repo = UserRepository(db_session)
    order_repo = OrderRepository(db_session)

    user = user_repo.create(email='u@example.com', hashed_password='hash')
    order = order_repo.create(external_id='EXT1', customer_id=user.id)

    service = OrderService(db_session)
    updated = service.transition(order.id, OrderStatus.CONFIRMED, actor_user_id=user.id)
    assert updated.status == OrderStatus.CONFIRMED

    # transition to SHIPPED by admin should be allowed
    admin = user_repo.create(email='admin@example.com', hashed_password='hash')
    admin.role = 'admin'
    db_session.add(admin)
    db_session.commit()

    updated = service.transition(order.id, OrderStatus.SHIPPED, actor_user_id=admin.id)
    assert updated.status == OrderStatus.SHIPPED

    # audit events written
    evs = db_session.query(OrderStatusEvent).filter(OrderStatusEvent.order_id == order.id).all()
    assert len(evs) >= 2


def test_invalid_transition(db_session):
    user_repo = UserRepository(db_session)
    order_repo = OrderRepository(db_session)

    user = user_repo.create(email='u2@example.com', hashed_password='hash')
    order = order_repo.create(external_id='EXT2', customer_id=user.id)

    service = OrderService(db_session)

    # attempt to skip to SHIPPED directly
    with pytest.raises(Exception):
        service.transition(order.id, OrderStatus.SHIPPED, actor_user_id=user.id)
