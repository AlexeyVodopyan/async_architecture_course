"""user

Revision ID: a21a2be0eff5
Revises:
Create Date: 2024-03-04 01:19:46.044177

"""
# stdlib
from typing import Sequence, Union

# thirdparty
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a21a2be0eff5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "email", sa.String(), nullable=False, comment="Email of user"
        ),
        sa.Column(
            "first_name",
            sa.String(),
            nullable=True,
            comment="First Name of user",
        ),
        sa.Column(
            "last_name",
            sa.String(),
            nullable=True,
            comment="Last Name of user",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            comment="Is this user active or not",
        ),
        sa.Column(
            "role",
            sa.Enum("PARROT", "MANAGER", "ACCOUNTANT", name="role"),
            nullable=False,
            comment="User Role",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Creation date",
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Modified date",
        ),
        sa.PrimaryKeyConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    op.execute("DROP TYPE role")
    # ### end Alembic commands ###
