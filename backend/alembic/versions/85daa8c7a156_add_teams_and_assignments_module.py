"""add_teams_and_assignments_module

Revision ID: 85daa8c7a156
Revises: 1b86f570ca4e
Create Date: 2026-11-10 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85daa8c7a156'
down_revision = '1b86f570ca4e'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create the new 'teams' table
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)
    op.create_index(op.f('ix_teams_name'), 'teams', ['name'], unique=True)

    # 2. Modify 'assignments' table using SQLite batch mode
    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reference_code', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('team_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.alter_column('status',
                   existing_type=sa.VARCHAR(),
                   type_=sa.Text(),
                   existing_nullable=True)
        batch_op.create_index(batch_op.f('ix_assignments_reference_code'), ['reference_code'], unique=True)
        batch_op.create_foreign_key('fk_assignments_team_id_teams', 'teams', ['team_id'], ['id'])
        batch_op.drop_column('assignee_name')
        batch_op.drop_column('notes')
        batch_op.drop_column('assigned_at')

    # 3. Modify 'responses' table using SQLite batch mode
    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_responses_coordinator_id_users', 'users', ['coordinator_id'], ['id'])

    # 4. Modify 'users' table using SQLite batch mode
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active',
                   existing_type=sa.BOOLEAN(),
                   type_=sa.Integer(),
                   existing_nullable=True)


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active',
                   existing_type=sa.Integer(),
                   type_=sa.BOOLEAN(),
                   existing_nullable=True)

    with op.batch_alter_table('responses', schema=None) as batch_op:
        batch_op.drop_constraint('fk_responses_coordinator_id_users', type_='foreignkey')

    with op.batch_alter_table('assignments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('assigned_at', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('notes', sa.TEXT(), nullable=True))
        batch_op.add_column(sa.Column('assignee_name', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint('fk_assignments_team_id_teams', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_assignments_reference_code'))
        batch_op.alter_column('status',
                   existing_type=sa.Text(),
                   type_=sa.VARCHAR(),
                   existing_nullable=True)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('description')
        batch_op.drop_column('team_id')
        batch_op.drop_column('reference_code')

    op.drop_index(op.f('ix_teams_name'), table_name='teams')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')