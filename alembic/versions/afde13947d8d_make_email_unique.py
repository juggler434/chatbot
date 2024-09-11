"""make email unique

Revision ID: afde13947d8d
Revises: 5293a983997f
Create Date: 2024-09-10 21:53:27.350257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afde13947d8d'
down_revision: Union[str, None] = '5293a983997f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("unique_user_email", "users", ["email"])


def downgrade() -> None:
    pass
