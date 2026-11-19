
import os

# Set test environment before importing application settings.
os.environ["APP_ENV"] = "test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.main import app

from app.models import User, Room, Member, Notification


@pytest.fixture(scope="session")
def test_engine():
    database_url = settings.TEST_DATABASE_URL

    if not database_url:
        pytest.fail("TEST_DATABASE_URL is not configured.")

    if database_url == settings.DATABASE_URL:
        pytest.fail("Test database must be different from development database.")

    engine = create_engine(database_url)

    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar()

    if database_name != "roomsync_test_db":
        engine.dispose()
        pytest.fail(
            f"Unsafe database selected: {database_name}. "
            "Expected roomsync_test_db."
        )

    # These operations are restricted to the verified test database.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    outer_transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint",
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        outer_transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def user_one(db_session):
    user = User(
        username="test_user_one",
        email="testone@example.com",
        password_hash=hash_password("TestPassword123"),
        full_name="Test User One",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def user_two(db_session):
    user = User(
        username="test_user_two",
        email="testtwo@example.com",
        password_hash=hash_password("TestPassword456"),
        full_name="Test User Two",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def room_one(db_session):
    room = Room(
        name="Automated Test Room",
        description="Room used for automated testing",
    )
    db_session.add(room)
    db_session.flush()
    return room


@pytest.fixture
def member_one(db_session, user_one, room_one):
    member = Member(
        name="Test User One",
        room_id=room_one.id,
        user_id=user_one.id,
        role="owner",
        is_active=True,
    )
    db_session.add(member)
    db_session.flush()
    return member


@pytest.fixture
def notification_one(db_session, member_one):
    notification = Notification(
        member_id=member_one.id,
        title="Test Notification",
        message="Automated notification test",
        notification_type="task_assignment",
        is_read=False,
    )
    db_session.add(notification)
    db_session.flush()
    return notification


@pytest.fixture
def token_one(user_one):
    return create_access_token(user_one.id)


@pytest.fixture
def token_two(user_two):
    return create_access_token(user_two.id)
