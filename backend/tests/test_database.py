from app.core.database import create_database_engine


def test_sqlite_database_engine_is_supported():
    engine = create_database_engine("sqlite://")
    try:
        assert engine.dialect.name == "sqlite"
    finally:
        engine.dispose()


def test_postgresql_database_engine_uses_psycopg_driver():
    engine = create_database_engine("postgresql://user:password@localhost/caseloop")
    try:
        assert engine.dialect.name == "postgresql"
        assert engine.dialect.driver == "psycopg"
    finally:
        engine.dispose()
