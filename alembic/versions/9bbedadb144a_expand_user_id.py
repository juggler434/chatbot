"""expand user id


Revision ID: 9bbedadb144a
Revises: b3e48fc7d13b
Create Date: 2024-09-11 23:24:29.954088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bbedadb144a'
down_revision: Union[str, None] = 'b3e48fc7d13b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
            table_name="messages",
            column_name="user_id",
            type_=sa.String(34))


def downgrade() -> None:
    pass
