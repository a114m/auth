"""empty message

Revision ID: 58c869af6093
Revises: None
Create Date: 2018-08-02 14:17:11.174669

"""

# revision identifiers, used by Alembic.
revision = '58c869af6093'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=True)
    op.create_table('resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('groups', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_name'), 'resources', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.String(length=24), nullable=False),
    sa.Column('groups', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index(op.f('ix_resources_name'), table_name='resources')
    op.drop_table('resources')
    op.drop_index(op.f('ix_groups_name'), table_name='groups')
    op.drop_table('groups')
    # ### end Alembic commands ###
