"""Initial migration.

Revision ID: 47e213847f0f
Revises: 
Create Date: 2022-04-22 19:35:46.722358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47e213847f0f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blooddonors', sa.Column('takenby', sa.String(length=20), nullable=True))
    op.alter_column('blooddonors', 'stat',
               existing_type=sa.TEXT(length=250),
               nullable=False)
    op.create_foreign_key(None, 'blooddonors', 'receivers', ['takenby'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blooddonors', type_='foreignkey')
    op.alter_column('blooddonors', 'stat',
               existing_type=sa.TEXT(length=250),
               nullable=True)
    op.drop_column('blooddonors', 'takenby')
    # ### end Alembic commands ###
