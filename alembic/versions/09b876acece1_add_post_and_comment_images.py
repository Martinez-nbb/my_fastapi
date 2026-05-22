"""add post and comment images

Revision ID: 09b876acece1
Revises: 6b4257a01b86
Create Date: 2026-05-22 09:40:05.442221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09b876acece1'
down_revision: Union[str, Sequence[str], None] = '6b4257a01b86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('blog_post_image',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.Column('original_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['application.blog_post.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='application'
    )
    op.create_index(op.f('ix_application_blog_post_image_post_id'), 'blog_post_image', ['post_id'], unique=False, schema='application')

    op.create_table('blog_comment_image',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('comment_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.Column('original_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['application.blog_comment.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='application'
    )
    op.create_index(op.f('ix_application_blog_comment_image_comment_id'), 'blog_comment_image', ['comment_id'], unique=False, schema='application')

    op.drop_column('blog_post', 'image', schema='application')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('blog_post', sa.Column('image', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=True), schema='application')
    op.drop_index(op.f('ix_application_blog_comment_image_comment_id'), table_name='blog_comment_image', schema='application')
    op.drop_table('blog_comment_image', schema='application')
    op.drop_index(op.f('ix_application_blog_post_image_post_id'), table_name='blog_post_image', schema='application')
    op.drop_table('blog_post_image', schema='application')
