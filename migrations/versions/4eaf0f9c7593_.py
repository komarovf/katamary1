"""empty message

Revision ID: 4eaf0f9c7593
Revises: None
Create Date: 2015-09-13 12:16:41.200357

"""

# revision identifiers, used by Alembic.
revision = '4eaf0f9c7593'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('_password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('survey_name', sa.String(length=128), nullable=True),
    sa.Column('intro_text', sa.String(length=999), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_survey_end_time'), 'survey', ['end_time'], unique=False)
    op.create_index(op.f('ix_survey_intro_text'), 'survey', ['intro_text'], unique=False)
    op.create_index(op.f('ix_survey_start_time'), 'survey', ['start_time'], unique=False)
    op.create_index(op.f('ix_survey_survey_name'), 'survey', ['survey_name'], unique=False)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('consecutive_number', sa.Integer(), nullable=True),
    sa.Column('q_object', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('respondent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('survey_id', sa.Integer(), nullable=False),
    sa.Column('sent_status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['survey_id'], ['survey.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('answer', sa.String(length=250), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_timestamp'), 'answer', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_answer_timestamp'), table_name='answer')
    op.drop_table('answer')
    op.drop_table('respondent')
    op.drop_table('question')
    op.drop_index(op.f('ix_survey_survey_name'), table_name='survey')
    op.drop_index(op.f('ix_survey_start_time'), table_name='survey')
    op.drop_index(op.f('ix_survey_intro_text'), table_name='survey')
    op.drop_index(op.f('ix_survey_end_time'), table_name='survey')
    op.drop_table('survey')
    op.drop_table('user')
    ### end Alembic commands ###
