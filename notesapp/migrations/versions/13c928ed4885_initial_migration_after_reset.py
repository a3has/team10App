"""Initial migration after reset.

Revision ID: 13c928ed4885
Revises: 
Create Date: 2023-11-19 22:11:05.556343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13c928ed4885'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=500),
               existing_nullable=False)

    with op.batch_alter_table('note_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=50), nullable=True))
        batch_op.alter_column('body',
               existing_type=sa.VARCHAR(length=140),
               type_=sa.String(length=200),
               existing_nullable=True)

    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('note_post', schema=None) as batch_op:
        batch_op.alter_column('body',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=140),
               existing_nullable=True)
        batch_op.drop_column('title')

    with op.batch_alter_table('note', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###
