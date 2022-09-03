"""empty message

Revision ID: 994c0f7db59f
Revises: 
Create Date: 2022-09-02 22:23:10.397191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '994c0f7db59f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', sa.Integer()),
        sa.Column('username', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('password', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
