"""add foreign key to post table

Revision ID: f5c9b8fd5f2f
Revises: 3c52df13600a
Create Date: 2022-06-24 17:16:23.401704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5c9b8fd5f2f'
down_revision = '3c52df13600a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('post', 'owner_id')
    pass
