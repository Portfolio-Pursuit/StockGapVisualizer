"""Add_new_column_to_user

Revision ID: db3e5e262f3a
Revises: 
Create Date: 2023-09-09 17:28:12.390431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db3e5e262f3a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user', sa.Column('new_column_name', sa.String(length=50), nullable=True))

def downgrade():
    op.drop_column('user', 'new_column_name')