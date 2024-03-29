"""empty message

Revision ID: fe34bdb089ff
Revises: bdaabad7ef06
Create Date: 2022-04-23 04:32:15.937201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe34bdb089ff'
down_revision = 'bdaabad7ef06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('blooddonors', 'stat',
               existing_type=sa.TEXT(length=250),
               nullable=False)
    op.create_foreign_key(None, 'blooddonors', 'receivers', ['takenby'], ['id'])
    op.add_column('receivers', sa.Column('hosname', sa.String(length=30), nullable=False))
    op.add_column('receivers', sa.Column('city', sa.String(length=20), nullable=False))
    op.drop_column('receivers', 'cnic')
    op.drop_column('receivers', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receivers', sa.Column('name', sa.VARCHAR(length=20), nullable=True))
    op.add_column('receivers', sa.Column('cnic', sa.VARCHAR(length=13), nullable=True))
    op.drop_column('receivers', 'city')
    op.drop_column('receivers', 'hosname')
    op.drop_constraint(None, 'blooddonors', type_='foreignkey')
    op.alter_column('blooddonors', 'stat',
               existing_type=sa.TEXT(length=250),
               nullable=True)
    # ### end Alembic commands ###
