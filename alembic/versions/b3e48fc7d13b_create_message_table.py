"""create message table

Revision ID: b3e48fc7d13b
Revises: afde13947d8d
Create Date: 2024-09-11 12:57:46.911782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3e48fc7d13b'
down_revision: Union[str, None] = 'afde13947d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'messages',
        sa.Column('id', sa.Uuid, primary_key=True),
        sa.Column('user_id', sa.String(16), nullable=False),
        sa.Column('question', sa.String(255)),
        sa.Column('response', sa.String(255)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime())
            )


def downgrade() -> None:
    op.drop_table('messages')
