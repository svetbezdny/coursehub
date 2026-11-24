"""create favorite_courses

Revision ID: 8f1a47a5907f
Revises: a745d0fda379
Create Date: 2026-11-21 14:23:23.083763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '8f1a47a5907f'
down_revision: Union[str, Sequence[str], None] = 'a745d0fda379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('favorite_courses',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'course_id', name='uq_favorite_courses_user_course')
    )
    op.create_index(op.f('ix_favorite_courses_course_id'), 'favorite_courses', ['course_id'], unique=False)
    op.create_index(op.f('ix_favorite_courses_user_id'), 'favorite_courses', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_favorite_courses_user_id'), table_name='favorite_courses')
    op.drop_index(op.f('ix_favorite_courses_course_id'), table_name='favorite_courses')
    op.drop_table('favorite_courses')
