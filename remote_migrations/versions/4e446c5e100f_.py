"""empty message

Revision ID: 4e446c5e100f
Revises: 736f39b16032
Create Date: 2018-07-08 20:27:08.522290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e446c5e100f'
down_revision = '736f39b16032'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('blocs_platform_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'blocs_platforms', ['blocs_platform_id'], ['id'])
    op.drop_column('users', 'blocs_platform')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('blocs_platform', sa.VARCHAR(length=16), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'blocs_platform_id')
    # ### end Alembic commands ###