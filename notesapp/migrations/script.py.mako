"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

# Use the optional `context` dictionary to get variables passed to the template
context = op.get_context()

# Define a new column to be added
new_column = sa.Column('name', sa.String(length=100), nullable=False)


def upgrade():
    ${upgrades if upgrades else "pass"}
    op.add_column('note', new_column)

def downgrade():
    ${downgrades if downgrades else "pass"}
    op.drop_column('note', 'name')
