"""empty message

Revision ID: 82ad7f8b5ebd
Revises: 
Create Date: 2020-07-14 10:51:03.094030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82ad7f8b5ebd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('responses',
    sa.Column('response_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('q1', sa.String(length=512), nullable=True),
    sa.Column('q2', sa.String(length=512), nullable=True),
    sa.Column('q3', sa.String(length=512), nullable=True),
    sa.Column('q4', sa.String(length=512), nullable=True),
    sa.Column('q5', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('response_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('responses')
    # ### end Alembic commands ###
