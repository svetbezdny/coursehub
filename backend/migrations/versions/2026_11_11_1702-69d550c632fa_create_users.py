"""create users

Revision ID: 69d550c632fa
Revises: 2fbb5bf0f060
Create Date: 2026-11-11 17:02:56.781313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '69d550c632fa'
down_revision: Union[str, Sequence[str], None] = '2fbb5bf0f060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
