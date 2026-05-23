"""add refresh tokens table

Revision ID: d95a43aeae2a
Revises: 8b9b375b8a26
Create Date: 2026-05-23 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd95a43aeae2a'
down_revision: Union[str, Sequence[str], None] = '8b9b375b8a26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('auth_refresh_token',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('token', sa.String(128), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('is_revoked', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(['user_id'], ['application.auth_user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema='application',
    )
    op.create_index(
        op.f('ix_application_auth_refresh_token_token'),
        'auth_refresh_token',
        ['token'],
        unique=True,
        schema='application',
    )


def downgrade() -> None:
    op.drop_index(
        op.f('ix_application_auth_refresh_token_token'),
        table_name='auth_refresh_token',
        schema='application',
    )
    op.drop_table('auth_refresh_token', schema='application')
