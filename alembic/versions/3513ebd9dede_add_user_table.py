"""add user table

Revision ID: 3513ebd9dede
Revises: ba46754c614b
Create Date: 2022-08-12 02:37:43.785208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3513ebd9dede'
down_revision = 'ba46754c614b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                            )


def downgrade() -> None:
    op.drop_table('users')
