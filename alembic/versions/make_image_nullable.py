"""Make image column nullable in blog_post table

Revision ID: make_image_nullable
Revises: 57e2e0cab439
Create Date: 2026-05-07 15:43:00

"""
from alembic import op
import sqlalchemy as sa


revision = 'make_image_nullable'
down_revision = '57e2e0cab439'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('image',
                              existing_type=sa.String(),
                              nullable=True,
                              existing_server_default=False)


def downgrade() -> None:
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('image',
                              existing_type=sa.String(),
                              nullable=False,
                              existing_server_default=False)