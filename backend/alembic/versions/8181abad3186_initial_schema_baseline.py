"""Initial schema baseline

Revision ID: 8181abad3186
Revises: 
Create Date: 2026-08-16 12:48:39.802175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8181abad3186'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Initial schema baseline - tables already exist.
    This migration marks the starting point for future migrations.
    No operations needed as schema is already in place.
    """
    pass


def downgrade() -> None:
    """
    Cannot downgrade from baseline - this would require dropping all tables.
    Use Base.metadata.drop_all() if needed.
    """
    pass
