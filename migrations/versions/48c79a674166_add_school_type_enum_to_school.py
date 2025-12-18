"""Add school_type enum to school

Revision ID: 48c79a674166
Revises: 6d2a1ea04f06
Create Date: 2025-12-18 09:41:02.293114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48c79a674166'
down_revision = '6d2a1ea04f06'
branch_labels = None
depends_on = None


school_type_enum = sa.Enum(
    "federal", "estadual", "municipal", "privada",
    name="school_type_enum"
)

def upgrade():
    bind = op.get_bind()
    school_type_enum.create(bind, checkfirst=True)  # garante que o TYPE exista

    with op.batch_alter_table("schools") as batch_op:
        batch_op.add_column(sa.Column("type", school_type_enum, nullable=True))

    op.execute("UPDATE schools SET type = 'municipal' WHERE type IS NULL")

    with op.batch_alter_table("schools") as batch_op:
        batch_op.alter_column("type", nullable=False)

def downgrade():
    with op.batch_alter_table("schools") as batch_op:
        batch_op.drop_column("type")

    school_type_enum.drop(op.get_bind(), checkfirst=True)
