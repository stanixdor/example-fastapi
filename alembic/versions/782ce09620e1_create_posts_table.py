"""create posts table

Revision ID: 782ce09620e1
Revises: 
Create Date: 2022-08-12 02:23:35.783019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782ce09620e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
