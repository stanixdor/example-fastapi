"""add content table to posts table

Revision ID: ba46754c614b
Revises: 782ce09620e1
Create Date: 2022-08-12 02:32:33.225304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba46754c614b'
down_revision = '782ce09620e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
