"""tasks

Revision ID: 10e87f6aa926
Revises: b371fac19303
Create Date: 2020-10-28 16:16:24.962097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10e87f6aa926'
down_revision = 'b371fac19303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###