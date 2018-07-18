"""empty message

Revision ID: 38a277160223
Revises: 27965359fa8a
Create Date: 2018-07-18 22:04:17.607010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '38a277160223'
down_revision = '27965359fa8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('created_by_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['created_by_id'], ['id'])
    op.add_column('posts', sa.Column('created_by_id', sa.Integer(), nullable=True))
    op.drop_constraint('posts_ibfk_2', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['created_by_id'], ['id'])
    op.drop_column('posts', 'user_id')
    op.add_column('projects', sa.Column('created_by_id', sa.Integer(), nullable=True))
    op.drop_constraint('projects_ibfk_2', 'projects', type_='foreignkey')
    op.create_foreign_key(None, 'projects', 'users', ['created_by_id'], ['id'])
    op.drop_column('projects', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'projects', type_='foreignkey')
    op.create_foreign_key('projects_ibfk_2', 'projects', 'users', ['user_id'], ['id'])
    op.drop_column('projects', 'created_by_id')
    op.add_column('posts', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_ibfk_2', 'posts', 'users', ['user_id'], ['id'])
    op.drop_column('posts', 'created_by_id')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'created_by_id')
    # ### end Alembic commands ###
