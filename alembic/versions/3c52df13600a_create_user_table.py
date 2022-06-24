"""create user table

Revision ID: 3c52df13600a
Revises: c8578ce71da0
Create Date: 2022-06-24 17:06:43.203106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c52df13600a'
down_revision = 'c8578ce71da0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, nullable=False), 
                    sa.Column('email', sa.String, nullable=False), 
                    sa.Column('password', sa.String, nullable=False), 
                    sa.Column('created_at', 
                              sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), 
                              nullable=False), 
                    sa.PrimaryKeyConstraint('id'), 
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
