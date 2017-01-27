"""Add background offset to profiles

Revision ID: 2182d60340d
Revises: 275951252d
Create Date: 2014-06-29 21:31:45.097828

"""

# revision identifiers, used by Alembic.
revision = '2182d60340d'
down_revision = '275951252d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bgOffsetX', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('bgOffsetY', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'bgOffsetY')
    op.drop_column('user', 'bgOffsetX')
    ### end Alembic commands ###
