"""empty message

Revision ID: 03dc0f974cde
Revises: da3af31c2944
Create Date: 2018-07-10 11:25:57.964068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03dc0f974cde'
down_revision = 'da3af31c2944'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_url', sa.TEXT(), nullable=True))
    op.add_column('users', sa.Column('first_name', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'avatar_url')
    # ### end Alembic commands ###