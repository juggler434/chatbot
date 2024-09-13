"""add deleted_at column to messaage

Revision ID: 3b6617f42f62
Revises: cbef5be8bbb0
Create Date: 2024-09-12 20:03:44.592172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b6617f42f62'
down_revision: Union[str, None] = 'cbef5be8bbb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('messages', sa.Column('deleted_at', sa.DateTime))


def downgrade() -> None:
    op.drop_column('messages', 'deleted_at')
