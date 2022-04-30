"""empty message

Revision ID: 936c0d21f033
Revises: 8864b8ad3d1b
Create Date: 2022-04-23 11:58:29.443489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '936c0d21f033'
down_revision = '8864b8ad3d1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birth_date', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('speciality_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'users', 'speciality', ['speciality_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'speciality_id')
    op.drop_column('users', 'birth_date')
    # ### end Alembic commands ###