
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy import pool

from app.core.config import settings
from app.core.database import Base

# Import every model so SQLAlchemy registers all tables.
from app.models.user import User
from app.models.room import Room
from app.models.member import Member
from app.models.room_invitation import RoomInvitation
from app.models.task import Task
from app.models.rotation import Rotation
from app.models.task_exemption import TaskExemption
from app.models.presence import Presence
from app.models.notification import Notification


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata used by Alembic autogenerate.
target_metadata = Base.metadata


def get_database_url():
    """
    Use the DATABASE_URL from application settings.
    Never allow Alembic to run against the test database.
    """

    if settings.APP_ENV.lower() == "test":
        raise RuntimeError(
            "Alembic migrations cannot run in test environment."
        )

    if (
        settings.TEST_DATABASE_URL
        and settings.DATABASE_URL == settings.TEST_DATABASE_URL
    ):
        raise RuntimeError(
            "Alembic cannot use the configured test database."
        )

    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    database_url = get_database_url()

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
