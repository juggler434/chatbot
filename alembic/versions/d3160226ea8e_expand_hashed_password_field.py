"""expand hashed password field

Revision ID: d3160226ea8e
Revises: 3b6617f42f62
Create Date: 2024-09-12 22:26:27.917330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3160226ea8e'
down_revision: Union[str, None] = '3b6617f42f62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
            table_name="users",
            column_name="hashed_password",
            type_=sa.String(300))


def downgrade() -> None:
    pass
