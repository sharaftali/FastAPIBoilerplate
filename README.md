# FasstAPI Boilerplate API

## Packages

This project uses **poetry** for dependency management, the rest of the packages are listed in `pyproject.toml`.

## **my[py]**
[**my[py]**](https://mypy.readthedocs.io/en/stable/getting_started.html) must be used for static typing.

## Code Style

This project uses [black](https://github.com/psf/black) for enforcing a consistent code style. It can be executed with
```
poetry run black .
```

## Run locally with **Poetry**
```
poetry run src
```

## Docker
```
docker build .
```

```
docker compose up src
```

## Database

This services uses its own postgres database. The database named `db_name` (unless configured differently) needs to be created before running the service.

## Migrations
The project uses **alembic** as migration tool for the database.

### Autogenerated migrations

Any file that contains SQLAlchemy models need to be imported in the corresponding `alembic/env.py` file in order to be taken into account.

_Example:_

```
import src.rental_units.models
```
All the models contained in this module will be found by **alembic**

Then run:
```
poetry run alembic revision --autogenerate -m "users and items table"
```

Output (example):
```
Context impl PostgresqlImpl.
Will assume transactional DDL.
Detected added table 'users'
Detected added index 'ix_users_email' on '['email']'
Detected added index 'ix_users_id' on '['id']'
Detected added table 'items'
Detected added index 'ix_items_description' on '['description']'
Detected added index 'ix_items_id' on '['id']'
Detected added index 'ix_items_title' on '['title']'
  Generating /dev/backend/housing-component/src/core/db/alembic/versions/1676974292_ad61bd71aceb_users_and_items_table.py ...  done
  ```

The generated file must be edited and fixed according the needs, then run it:
```
poetry run alembic upgrade head
```
it can be also the revision instead of head: __1676974292__
```
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1676974292
```

More info: https://alembic.sqlalchemy.org/en/latest/autogenerate.html

### Manually generated migrations

```
poetry run alembic revision -m "create user table"
```
Output (example):
```
Generating .../alembic/versions/1975ea83b712_create_user_table.py...done
```

Then edit the file

```
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('type', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('users')
```

run it:

```
poetry run alembic upgrade head
```
it can be also the revision instead of head: __1975ea83b712__

Returns (example):
```
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

More info at: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
