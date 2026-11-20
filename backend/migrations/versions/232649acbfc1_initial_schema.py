
"""initial schema

Revision ID: 232649acbfc1
Revises:
Create Date: 2026-11-20 00:51:37.454613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '232649acbfc1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_rooms_id'),
        'rooms',
        ['id'],
        unique=False
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_users_email'),
        'users',
        ['email'],
        unique=True
    )
    op.create_index(
        op.f('ix_users_id'),
        'users',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_users_username'),
        'users',
        ['username'],
        unique=True
    )

    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_irregular', sa.Boolean(), nullable=False),
        sa.Column('total_tasks_completed', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_members_id'),
        'members',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_members_room_id'),
        'members',
        ['room_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_members_user_id'),
        'members',
        ['user_id'],
        unique=False
    )

    op.create_table(
        'room_invitations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('inviter_id', sa.Integer(), nullable=False),
        sa.Column('invitee_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('responded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['invitee_id'],
            ['users.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['inviter_id'],
            ['users.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_room_invitations_id'),
        'room_invitations',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_room_invitations_invitee_id'),
        'room_invitations',
        ['invitee_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_room_invitations_inviter_id'),
        'room_invitations',
        ['inviter_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_room_invitations_room_id'),
        'room_invitations',
        ['room_id'],
        unique=False
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('frequency', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_tasks_id'),
        'tasks',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_tasks_room_id'),
        'tasks',
        ['room_id'],
        unique=False
    )

    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('message', sa.String(length=500), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['member_id'],
            ['members.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_notifications_id'),
        'notifications',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_notifications_member_id'),
        'notifications',
        ['member_id'],
        unique=False
    )

    op.create_table(
        'presence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('is_present', sa.Boolean(), nullable=False),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['member_id'],
            ['members.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_presence_id'),
        'presence',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_presence_member_id'),
        'presence',
        ['member_id'],
        unique=False
    )

    op.create_table(
        'rotations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('assignment_reason', sa.String(length=255), nullable=True),
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['member_id'],
            ['members.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['task_id'],
            ['tasks.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_rotations_id'),
        'rotations',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_rotations_member_id'),
        'rotations',
        ['member_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_rotations_room_id'),
        'rotations',
        ['room_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_rotations_task_id'),
        'rotations',
        ['task_id'],
        unique=False
    )

    op.create_table(
        'task_exemptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['member_id'],
            ['members.id'],
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['task_id'],
            ['tasks.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        op.f('ix_task_exemptions_id'),
        'task_exemptions',
        ['id'],
        unique=False
    )
    op.create_index(
        op.f('ix_task_exemptions_member_id'),
        'task_exemptions',
        ['member_id'],
        unique=False
    )
    op.create_index(
        op.f('ix_task_exemptions_task_id'),
        'task_exemptions',
        ['task_id'],
        unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f('ix_task_exemptions_task_id'),
        table_name='task_exemptions'
    )
    op.drop_index(
        op.f('ix_task_exemptions_member_id'),
        table_name='task_exemptions'
    )
    op.drop_index(
        op.f('ix_task_exemptions_id'),
        table_name='task_exemptions'
    )
    op.drop_table('task_exemptions')

    op.drop_index(
        op.f('ix_rotations_task_id'),
        table_name='rotations'
    )
    op.drop_index(
        op.f('ix_rotations_room_id'),
        table_name='rotations'
    )
    op.drop_index(
        op.f('ix_rotations_member_id'),
        table_name='rotations'
    )
    op.drop_index(
        op.f('ix_rotations_id'),
        table_name='rotations'
    )
    op.drop_table('rotations')

    op.drop_index(
        op.f('ix_presence_member_id'),
        table_name='presence'
    )
    op.drop_index(
        op.f('ix_presence_id'),
        table_name='presence'
    )
    op.drop_table('presence')

    op.drop_index(
        op.f('ix_notifications_member_id'),
        table_name='notifications'
    )
    op.drop_index(
        op.f('ix_notifications_id'),
        table_name='notifications'
    )
    op.drop_table('notifications')

    op.drop_index(
        op.f('ix_tasks_room_id'),
        table_name='tasks'
    )
    op.drop_index(
        op.f('ix_tasks_id'),
        table_name='tasks'
    )
    op.drop_table('tasks')

    op.drop_index(
        op.f('ix_room_invitations_room_id'),
        table_name='room_invitations'
    )
    op.drop_index(
        op.f('ix_room_invitations_inviter_id'),
        table_name='room_invitations'
    )
    op.drop_index(
        op.f('ix_room_invitations_invitee_id'),
        table_name='room_invitations'
    )
    op.drop_index(
        op.f('ix_room_invitations_id'),
        table_name='room_invitations'
    )
    op.drop_table('room_invitations')

    op.drop_index(
        op.f('ix_members_user_id'),
        table_name='members'
    )
    op.drop_index(
        op.f('ix_members_room_id'),
        table_name='members'
    )
    op.drop_index(
        op.f('ix_members_id'),
        table_name='members'
    )
    op.drop_table('members')

    op.drop_index(
        op.f('ix_users_username'),
        table_name='users'
    )
    op.drop_index(
        op.f('ix_users_id'),
        table_name='users'
    )
    op.drop_index(
        op.f('ix_users_email'),
        table_name='users'
    )
    op.drop_table('users')

    op.drop_index(
        op.f('ix_rooms_id'),
        table_name='rooms'
    )
    op.drop_table('rooms')
