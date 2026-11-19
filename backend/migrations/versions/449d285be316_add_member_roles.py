
"""add member roles

Revision ID: 449d285be316
Revises: 232649acbfc1
Create Date: 2026-11-20 01:05:58.263472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "449d285be316"
down_revision: Union[str, Sequence[str], None] = "232649acbfc1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add member roles and preserve existing room ownership."""

    op.add_column(
        "members",
        sa.Column(
            "role",
            sa.String(length=20),
            server_default="member",
            nullable=False,
        ),
    )

    connection = op.get_bind()

    room_exists = connection.execute(
        sa.text(
            "SELECT EXISTS (SELECT 1 FROM rooms WHERE id = 1)"
        )
    ).scalar()

    # Fresh databases have no existing rooms.
    if not room_exists:
        return

    member_exists = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM members
                WHERE id = 1
                  AND room_id = 1
                  AND user_id = 1
            )
            """
        )
    ).scalar()

    if not member_exists:
        raise RuntimeError(
            "Cannot assign room ownership: expected Member ID 1, "
            "Room ID 1 and User ID 1 mapping was not found."
        )

    connection.execute(
        sa.text(
            """
            UPDATE members
            SET role = 'owner'
            WHERE id = 1
              AND room_id = 1
              AND user_id = 1
            """
        )
    )


def downgrade() -> None:
    """Remove member roles."""

    op.drop_column("members", "role")
