"""Add watchlist relationship to User model

Revision ID: dc01301b7502
Revises: feb1122a2a9c
Create Date: 2023-09-10 20:56:39.512841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc01301b7502'
down_revision: Union[str, None] = 'feb1122a2a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.create_foreign_key('fk_user_watchlist', 'watchlist', ['user_id'], ['id'])
        

def downgrade() -> None:
    pass
