"""Create Partner table

Revision ID: 7c3fcb0748c7
Revises: 
Create Date: 2022-01-20 06:25:19.746436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c3fcb0748c7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('partner', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('partnername', sa.String(), nullable=False),
        sa.Column('partnerfunction', sa.String(), nullable=False, server_default="Supplier"),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=True),
        sa.Column('createdtime', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()') ,nullable=False))
    pass


def downgrade():
    op.drop_table('partner')

    pass
