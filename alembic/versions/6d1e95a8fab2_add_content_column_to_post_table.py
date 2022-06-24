"""add content column to post table

Revision ID: 6d1e95a8fab2
Revises: 05ced7f6a560
Create Date: 2022-06-24 16:55:08.845881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d1e95a8fab2'
down_revision = '05ced7f6a560'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
