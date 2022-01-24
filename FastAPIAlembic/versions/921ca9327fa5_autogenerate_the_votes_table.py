"""Autogenerate the Votes table

Revision ID: 921ca9327fa5
Revises: 588df9b7cb05
Create Date: 2022-01-21 06:54:58.950156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '921ca9327fa5'
down_revision = '588df9b7cb05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['partner_id'], ['partner.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('partner_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###