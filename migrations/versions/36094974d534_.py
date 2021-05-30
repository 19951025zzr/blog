"""empty message

Revision ID: 36094974d534
Revises: 29c91a06a468
Create Date: 2021-05-28 16:23:46.249771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36094974d534'
down_revision = '29c91a06a468'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###