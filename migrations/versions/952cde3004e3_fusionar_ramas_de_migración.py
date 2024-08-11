"""Fusionar ramas de migración

Revision ID: 952cde3004e3
Revises: 2d27f12973b3, 3cdd8c182156, dc51322d4ed5
Create Date: 2024-08-11 18:37:45.147974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '952cde3004e3'
down_revision = ('2d27f12973b3', '3cdd8c182156', 'dc51322d4ed5')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
