from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'languages',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('name', sa.String(64), unique=True, nullable=False)
    )

    op.create_table(
        'words',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('text', sa.String(128), nullable=False),
        sa.Column('language_id', sa.Integer, sa.ForeignKey('languages.id'), nullable=False)
    )

    op.create_table(
        'translations',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('word_id', sa.Integer, sa.ForeignKey('words.id'), nullable=False),
        sa.Column('target_language_id', sa.Integer, sa.ForeignKey('languages.id'), nullable=False),
        sa.Column('translation_text', sa.String(128), nullable=False),
        sa.UniqueConstraint('word_id', 'target_language_id', name='unique_word_translation')
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('username', sa.String(64), unique=True, nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('native_language_id', sa.Integer, sa.ForeignKey('languages.id')),
        sa.Column('learning_language_id', sa.Integer, sa.ForeignKey('languages.id'))
    )

    op.create_table(
        'usertranslations',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('status', sa.Integer, default=0),
        sa.Column('translation_id', sa.Integer, sa.ForeignKey('translations.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.UniqueConstraint('user_id', 'translation_id', name='unique_user_translation')
    )

def downgrade():
    op.drop_table('usertranslations')
    op.drop_table('users')
    op.drop_table('translations')
    op.drop_table('words')
    op.drop_table('languages')
