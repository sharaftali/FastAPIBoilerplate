"""init

Revision ID: 3019b55e0ff5
Revises: 
Create Date: 2024-01-26 16:21:53.017545

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3019b55e0ff5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "addresses",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("street", sa.VARCHAR(length=255), nullable=True),
        sa.Column("postal_code", sa.VARCHAR(length=10), nullable=True),
        sa.Column("city", sa.VARCHAR(length=255), nullable=True),
        sa.Column("state", sa.VARCHAR(length=255), nullable=True),
        sa.Column("country", sa.VARCHAR(length=2), nullable=True),
        sa.Column("lat", sa.FLOAT(asdecimal=True), nullable=True),
        sa.Column("lng", sa.FLOAT(asdecimal=True), nullable=True),
        sa.CheckConstraint("octet_length(id) <= 40", name="id_byte_limit"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.String(length=63), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column(
            "permission",
            postgresql.ENUM("IS_OPERATOR", name="permissionenum"),
            nullable=False,
        ),
        sa.Column("address", sa.String(), nullable=True),
        sa.CheckConstraint(
            "id ~* '^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$'",
            name="id_format_check",
        ),
        sa.ForeignKeyConstraint(
            ["address"],
            ["addresses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    op.drop_table("addresses")
    # ### end Alembic commands ###
