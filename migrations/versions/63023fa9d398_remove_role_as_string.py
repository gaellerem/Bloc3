"""remove role as string

Revision ID: 63023fa9d398
Revises: 6c7ed9c3727d
Create Date: 2024-09-05 16:15:04.367716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63023fa9d398'
down_revision = '6c7ed9c3727d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=80), nullable=False))

    # ### end Alembic commands ###
