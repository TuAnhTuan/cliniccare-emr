"""add gender to patients

Revision ID: 0cd27c1ae23d
Revises: 4efecd315462
Create Date: 2026-09-06 22:07:59.694888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cd27c1ae23d'
down_revision: Union[str, None] = '4efecd315462'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('patients', sa.Column('gender', sa.String(length=10), nullable=True))


def downgrade() -> None:
    op.drop_column('patients', 'gender')
