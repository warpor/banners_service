"""initial

Revision ID: 95d95652c481
Revises: 
Create Date: 2024-04-14 21:58:13.473674

"""
from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '95d95652c481'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('accesstoken',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('token', sa.String(length=43), nullable=False),
    sa.Column('created_at', fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_index(op.f('ix_accesstoken_created_at'), 'accesstoken', ['created_at'], unique=False)
    op.create_table('banners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['feature_id'], ['features.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('banners_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('banner_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['banner_id'], ['banners.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_banners_tags_id'), 'banners_tags', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_banners_tags_id'), table_name='banners_tags')
    op.drop_table('banners_tags')
    op.drop_table('banners')
    op.drop_index(op.f('ix_accesstoken_created_at'), table_name='accesstoken')
    op.drop_table('accesstoken')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('features')
    # ### end Alembic commands ###