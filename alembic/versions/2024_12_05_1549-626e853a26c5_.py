"""empty message

Revision ID: 626e853a26c5
Revises: 
Create Date: 2024-12-05 15:49:01.320915

"""
from typing import Sequence, Union

import sqlalchemy as sa

import src
from alembic import op



# revision identifiers, used by Alembic.
revision: str = '626e853a26c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('legal_entity',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('ogrn', sa.String(length=13), nullable=False),
    sa.Column('ogrnip', sa.String(length=15), nullable=True),
    sa.Column('inn', sa.String(length=10), nullable=False),
    sa.Column('subscription_expiration_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_legal_entity')),
    sa.UniqueConstraint('id', name=op.f('uq_legal_entity_id'))
    )
    op.create_index(op.f('ix_legal_entity_email'), 'legal_entity', ['email'], unique=True)
    op.create_index(op.f('ix_legal_entity_inn'), 'legal_entity', ['inn'], unique=True)
    op.create_index(op.f('ix_legal_entity_name'), 'legal_entity', ['name'], unique=True)
    op.create_index(op.f('ix_legal_entity_ogrn'), 'legal_entity', ['ogrn'], unique=True)
    op.create_index(op.f('ix_legal_entity_ogrnip'), 'legal_entity', ['ogrnip'], unique=True)
    op.create_table('feedback_about_client',
    sa.Column('email_of_client', sa.String(length=255), nullable=True),
    sa.Column('first_name_of_client', sa.String(length=100), nullable=True),
    sa.Column('last_name_of_client', sa.String(length=100), nullable=True),
    sa.Column('middle_name_of_client', sa.String(length=100), nullable=True),
    sa.Column('number_phone_of_client', sa.String(length=100), nullable=True),
    sa.Column('telegram_nickname_of_client', sa.String(length=255), nullable=True),
    sa.Column('legal_entity_id', sa.UUID(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.ForeignKeyConstraint(['legal_entity_id'], ['legal_entity.id'], name=op.f('fk_feedback_about_client_legal_entity_id_legal_entity'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_feedback_about_client')),
    sa.UniqueConstraint('id', name=op.f('uq_feedback_about_client_id'))
    )
    op.create_index(op.f('ix_feedback_about_client_email_of_client'), 'feedback_about_client', ['email_of_client'], unique=False)
    op.create_index(op.f('ix_feedback_about_client_number_phone_of_client'), 'feedback_about_client', ['number_phone_of_client'], unique=False)
    op.create_table('payment',
    sa.Column('is_confirmed', sa.Boolean(), nullable=False),
    sa.Column('payment_id', sa.UUID(), nullable=False),
    sa.Column('legal_entity_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.ForeignKeyConstraint(['legal_entity_id'], ['legal_entity.id'], name=op.f('fk_payment_legal_entity_id_legal_entity'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('payment_id', 'id', name=op.f('pk_payment')),
    sa.UniqueConstraint('id', name=op.f('uq_payment_id')),
    sa.UniqueConstraint('payment_id', name=op.f('uq_payment_payment_id'))
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('role', sa.Enum('employee', 'org_admin', name='user_role_enum', native_enum=False), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('legal_entity_id', sa.UUID(), nullable=False),
    sa.Column('is_registered', sa.Boolean(), nullable=True),
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.ForeignKeyConstraint(['legal_entity_id'], ['legal_entity.id'], name=op.f('fk_users_legal_entity_id_legal_entity'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('id', name=op.f('uq_users_id'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('payment')
    op.drop_index(op.f('ix_feedback_about_client_number_phone_of_client'), table_name='feedback_about_client')
    op.drop_index(op.f('ix_feedback_about_client_email_of_client'), table_name='feedback_about_client')
    op.drop_table('feedback_about_client')
    op.drop_index(op.f('ix_legal_entity_ogrnip'), table_name='legal_entity')
    op.drop_index(op.f('ix_legal_entity_ogrn'), table_name='legal_entity')
    op.drop_index(op.f('ix_legal_entity_name'), table_name='legal_entity')
    op.drop_index(op.f('ix_legal_entity_inn'), table_name='legal_entity')
    op.drop_index(op.f('ix_legal_entity_email'), table_name='legal_entity')
    op.drop_table('legal_entity')
    # ### end Alembic commands ###