"""change course price to numeric

Revision ID: 00e808cea527
Revises: 69d550c632fa
Create Date: 2026-11-11 21:51:14.928157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '00e808cea527'
down_revision: Union[str, Sequence[str], None] = '69d550c632fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("courses") as batch_op:
        batch_op.alter_column('price',
                existing_type=sa.FLOAT(),
                type_=sa.Numeric(precision=10, scale=2),
                existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("courses") as batch_op:
        batch_op.alter_column('price',
                existing_type=sa.Numeric(precision=10, scale=2),
                type_=sa.FLOAT(),
                existing_nullable=False)
