from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

from app.core.database import Base, engine
from app.models import models


def initialize_database() -> None:
    existing_tables = set(inspect(engine).get_table_names())
    if "alembic_version" in existing_tables:
        command.upgrade(Config("alembic.ini"), "head")
        return
    if existing_tables:
        raise RuntimeError(
            "Refusing to initialize a non-empty database without Alembic history."
        )

    Base.metadata.create_all(bind=engine)
    command.stamp(Config("alembic.ini"), "head")


if __name__ == "__main__":
    initialize_database()
