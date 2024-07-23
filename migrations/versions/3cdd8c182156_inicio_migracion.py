"""inicio migracion

Revision ID: 3cdd8c182156
Revises: 
Create Date: 2024-07-22 22:23:37.590591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cdd8c182156'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipo_accesorios',
    sa.Column('equipo_id', sa.Integer(), nullable=False),
    sa.Column('accesorio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accesorio_id'], ['accesorio.id'], ),
    sa.ForeignKeyConstraint(['equipo_id'], ['equipo.id'], ),
    sa.PrimaryKeyConstraint('equipo_id', 'accesorio_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipo_accesorios')
    # ### end Alembic commands ###