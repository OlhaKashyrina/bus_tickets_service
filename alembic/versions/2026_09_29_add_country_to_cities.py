"""Add country to cities

Revision ID: ba95d096022f
Revises: a5cf80d88ea4
Create Date: 2026-09-29 20:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ba95d096022f'
down_revision: str | Sequence[str] | None = 'a5cf80d88ea4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cities', sa.Column('country', sa.String(length=128), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cities', 'country')
