"""add foreign Key to Partner table

Revision ID: 588df9b7cb05
Revises: 4c7c2665d287
Create Date: 2022-01-21 01:48:18.244724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '588df9b7cb05'
down_revision = '4c7c2665d287'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('partner', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('partner_user_fk', source_table="partner", referent_table="users", 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('partner_user_fk', table_name='partner')
    op.drop_column('partner', 'owner_id')
    pass
