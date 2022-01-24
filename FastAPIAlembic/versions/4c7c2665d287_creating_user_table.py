"""creating User Table

Revision ID: 4c7c2665d287
Revises: 7c3fcb0748c7
Create Date: 2022-01-21 01:37:47.860536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c7c2665d287'
down_revision = '7c3fcb0748c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('createdtime', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()') ,nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))

        #this is another way to setup primary Key.

    pass


def downgrade():
    op.drop_table('users')

    pass
