"""expand user id again


Revision ID: cbef5be8bbb0
Revises: 9bbedadb144a
Create Date: 2024-09-11 23:36:58.662836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbef5be8bbb0'
down_revision: Union[str, None] = '9bbedadb144a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
            table_name="messages",
            column_name="user_id",
            type_=sa.String(40))


def downgrade() -> None:
    pass
