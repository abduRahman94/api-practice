"""empty message

Revision ID: 04c710032802
Revises: 142e88a055ed
Create Date: 2022-08-27 13:19:09.167111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04c710032802'
down_revision = '142e88a055ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('surname', sa.String(length=100), nullable=True),
    sa.Column('program', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('student')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('surname', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('program', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='student_pkey')
    )
    op.drop_table('students')
    # ### end Alembic commands ###