"""Add time stamp to File table

Revision ID: fcb22cbfa6f1
Revises: be9885c7ce2b
Create Date: 2022-04-18 11:46:33.921024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcb22cbfa6f1'
down_revision = 'be9885c7ce2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'created_at')
    # ### end Alembic commands ###
