"""Updated UserOrder table

Revision ID: 2a3d1cc3a796
Revises: 
Create Date: 2024-03-17 17:45:10.197783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3d1cc3a796'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userorder', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_amount', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('quantities', app.models.user.JsonEncodedDict(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userorder', schema=None) as batch_op:
        batch_op.drop_column('quantities')
        batch_op.drop_column('total_amount')

    # ### end Alembic commands ###
