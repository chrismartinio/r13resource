"""empty message

Revision ID: d2234de6db67
Revises: 
Create Date: 2019-08-24 02:09:38.901931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2234de6db67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lectures')
    op.drop_table('gitusers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gitusers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='gitusers_pkey')
    )
    op.create_table('lectures',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=300), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='lectures_pkey')
    )
    # ### end Alembic commands ###
