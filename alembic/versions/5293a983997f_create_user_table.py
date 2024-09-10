"""create user table

Revision ID: 5293a983997f
Revises: 
Create Date: 2024-09-10 13:27:39.331428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5293a983997f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
            'users',
            sa.Column('id', sa.Uuid, primary_key=True),
            sa.Column('email', sa.String(320), nullable=False),
            sa.Column('hashed_password', sa.String(72), nullable=False),
            )


def downgrade() -> None:
    op.drop_table('users')
