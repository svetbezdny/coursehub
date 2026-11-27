"""create reviews

Revision ID: ea7472a87a08
Revises: 8f1a47a5907f
Create Date: 2026-11-27 20:35:42.223528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'ea7472a87a08'
down_revision: Union[str, Sequence[str], None] = '8f1a47a5907f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('reviews',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'course_id', name='uq_reviews_user_course')
    )
    op.create_index(op.f('ix_reviews_course_id'), 'reviews', ['course_id'], unique=False)
    op.create_index(op.f('ix_reviews_user_id'), 'reviews', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_reviews_user_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_course_id'), table_name='reviews')
    op.drop_table('reviews')
