"""Added account table

Revision ID: b7a9e3375b45
Revises: 
Create Date: 2022-03-30 15:32:25.834436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b7a9e3375b45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f('ix_accounts_uuid'), 'accounts', ['uuid'], unique=False)
    op.create_foreign_key(None, 'accounts', 'users', ['user_id'], ['uuid'])
    op.create_foreign_key(None, 'accounts', 'currencies', ['currency_tag'], ['tag'])
    op.drop_column('accounts', 'id')
    op.add_column('currencies', sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f('ix_currencies_uuid'), 'currencies', ['uuid'], unique=False)
    op.add_column('transactions', sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_index(op.f('ix_transactions_uuid'), 'transactions', ['uuid'], unique=False)
    op.create_foreign_key(None, 'transactions', 'accounts', ['account_from_id'], ['uuid'])
    op.create_foreign_key(None, 'transactions', 'currencies', ['currency_tag'], ['tag'])
    op.create_foreign_key(None, 'transactions', 'accounts', ['account_to_id'], ['uuid'])
    op.drop_column('transactions', 'id')
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('activated', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=False)
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_column('users', 'activated')
    op.drop_column('users', 'admin')
    op.add_column('transactions', sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_index(op.f('ix_transactions_uuid'), table_name='transactions')
    op.drop_column('transactions', 'uuid')
    op.drop_index(op.f('ix_currencies_uuid'), table_name='currencies')
    op.drop_column('currencies', 'uuid')
    op.add_column('accounts', sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.drop_index(op.f('ix_accounts_uuid'), table_name='accounts')
    op.drop_column('accounts', 'uuid')
    # ### end Alembic commands ###
