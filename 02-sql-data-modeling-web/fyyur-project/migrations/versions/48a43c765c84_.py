"""empty message

Revision ID: 48a43c765c84
Revises: e8560fe9ee4b
Create Date: 2020-12-01 11:07:59.107823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48a43c765c84'
down_revision = 'e8560fe9ee4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('genres', sa.String(length=120), nullable=False))
    op.add_column('venues', sa.Column('website', sa.String(length=120), nullable=True))
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'genres')
    # ### end Alembic commands ###
