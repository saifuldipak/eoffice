"""Modify role column in users table

Revision ID: f66c93ce7392
Revises: b99036e2f3dc
Create Date: 2025-04-09 16:19:00.631777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f66c93ce7392'
down_revision: Union[str, None] = 'b99036e2f3dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Use batch mode to handle SQLite limitations
    with op.batch_alter_table('users', recreate='always') as batch_op:
        batch_op.alter_column('role',
                              existing_type=sa.VARCHAR(length=14),
                              type_=sa.Integer(),
                              nullable=True)
        batch_op.create_foreign_key('fk_users_role', 'roles', ['role'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Use batch mode to revert the column changes
    with op.batch_alter_table('users', recreate='always') as batch_op:
        batch_op.drop_constraint('fk_users_role', type_='foreignkey')
        batch_op.alter_column('role',
                              existing_type=sa.Integer(),
                              type_=sa.VARCHAR(length=14),
                              nullable=False)
