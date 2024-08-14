"""Description of changes

Revision ID: a4a598d42123
Revises: 7893d32110a7
Create Date: 2024-08-13 23:47:43.719484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4a598d42123'
down_revision: Union[str, None] = '7893d32110a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_Users_email', table_name='Users')
    op.create_index(op.f('ix_Users_email'), 'Users', ['email'], unique=False)
    op.drop_index('ix_Users_username', table_name='Users')
    op.create_index(op.f('ix_Users_username'), 'Users', ['username'], unique=False)
    op.create_index(op.f('ix_Users_role'), 'Users', ['role'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_role'), table_name='Users')
    op.drop_index(op.f('ix_Users_username'), table_name='Users')
    op.create_index('ix_Users_username', 'Users', ['username'], unique=True)
    op.drop_index(op.f('ix_Users_email'), table_name='Users')
    op.create_index('ix_Users_email', 'Users', ['email'], unique=True)
    # ### end Alembic commands ###

