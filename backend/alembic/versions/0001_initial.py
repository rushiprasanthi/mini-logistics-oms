"""initial

Revision ID: 0001
Revises: 
Create Date: 2026-05-17 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('role', sa.String(50), nullable=False, server_default=sa.text("'user'")),
    )

    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('external_id', sa.String(128), nullable=False, unique=True),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
    )

    op.create_table(
        'order_status_events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('from_status', sa.String(32), nullable=False),
        sa.Column('to_status', sa.String(32), nullable=False),
        sa.Column('performed_by', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('reason', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
    )


def downgrade():
    op.drop_table('order_status_events')
    op.drop_table('orders')
    op.drop_table('users')
