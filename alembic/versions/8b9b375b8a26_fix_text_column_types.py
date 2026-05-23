"""fix text column types

Revision ID: 8b9b375b8a26
Revises: 09b876acece1
Create Date: 2026-05-22 09:50:54.412268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b9b375b8a26'
down_revision: Union[str, Sequence[str], None] = '09b876acece1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('blog_post', 'text', type_=sa.Text(), schema='application')
    op.alter_column('blog_comment', 'text', type_=sa.Text(), schema='application')
    op.alter_column('blog_category', 'description', type_=sa.Text(), schema='application')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('blog_category', 'description', type_=sa.String(255), schema='application')
    op.alter_column('blog_comment', 'text', type_=sa.String(255), schema='application')
    op.alter_column('blog_post', 'text', type_=sa.String(255), schema='application')
