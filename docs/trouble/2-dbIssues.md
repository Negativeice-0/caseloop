# CaseLoop Backend & Database Troubleshooting Guide

This guide documents common pitfalls encountered during SQLAlchemy model creation, Alembic migration setup, and SQLite constraint handling while building the **CaseLoop** backend.

---

## 1. Missing Database / Model Modules

* **Error Example:** `ModuleNotFoundError: No module named 'app.core.database'` or `ImportError: cannot import name 'models' from 'app.models'`
* **Cause:** Trying to run scripts (like `seed.py`) before creating the underlying Python files, or failing to re-export modules inside `app/models/__init__.py`.
* **Fix:**
* Ensure `app/core/database.py` and `app/models/models.py` exist.
* Explicitly export models in `app/models/__init__.py` so parent packages can find them:
```python
from .models import Base, User, ResponseItem, ResponseEvent

```





---

## 2. SQLite Foreign Key & Constraint Limitations (`ALTER TABLE`)

* **Error Example:** `NotImplementedError: No support for ALTER of constraints in SQLite dialect.`
* **Cause:** Standard `ALTER TABLE` commands (like adding foreign keys or complex column alterations) are not natively supported by SQLite's query engine.
* **Fix:** Wrap your Alembic migration operations inside SQLite's **batch mode** (which performs a safe copy-and-move table rewrite under the hood):
```python
with op.batch_alter_table("responses", schema=None) as batch_op:
  batch_op.add_column(sa.Column("reference_code", sa.String(), nullable=False))
  batch_op.create_foreign_key(
      "fk_responses_coordinator_id_users", "users", ["coordinator_id"], ["id"]
  )

```



```

---

## 3. What does `alembic stamp head` mean?

When you hit the error where Alembic tried to create a table that already existed (`table response_events already exists`), it happened because your database and Alembic's version history got temporarily out of sync.

### The Git Analogy:
Think of Alembic like Git:
* Your database tables are like your **working directory files**.
* Alembic migration files are like your **Git commits**.
* The `alembic_version` table inside SQLite is like Git's pointer to the **current active commit hash (`HEAD`)**.

### What `stamp head` actually does:
If you make manual changes, test scripts, or partially apply a migration, your database might already have the tables/columns, but Alembic's tracker doesn't know it yet. 

Running `alembic stamp head` is the equivalent of telling Git: 
> *"Hey, don't try to re-apply these changes or run code statements. Just force-update your internal pointer (`HEAD`) to point to the latest migration version file, because the actual database state is already caught up."*

It safely syncs Alembic's tracking history with reality without executing SQL statements that would crash (like trying to create a table that's already there).

```