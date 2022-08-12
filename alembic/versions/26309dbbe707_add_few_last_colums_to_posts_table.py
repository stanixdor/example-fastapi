"""add few last colums to posts table

Revision ID: 26309dbbe707
Revises: 0fa0f085df34
Create Date: 2022-08-12 02:50:21.142011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26309dbbe707'
down_revision = '0fa0f085df34'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
