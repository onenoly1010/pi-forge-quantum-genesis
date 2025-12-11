# Alembic Migrations

This directory is reserved for Alembic database migrations.

## Setup

To initialize Alembic for database migrations:

```bash
# Initialize Alembic (creates alembic.ini and alembic directory)
alembic init migrations

# Edit alembic.ini to set your database URL or use environment variable
# Update env.py to import your models

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

## Migration Commands

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration version
alembic current

# Show migration history
alembic history
```

## Important Notes

1. **Development**: For local development with Docker Compose, the SQL schema in `sql/schema/001_initial_ledger.sql` is automatically applied on container startup.

2. **Production**: Always use Alembic migrations for production deployments. Never use AUTO_CREATE_TABLES=true in production.

3. **Testnet**: Run migrations manually before deploying to testnet:
   ```bash
   alembic upgrade head
   ```

4. **Mainnet**: Migrations require guardian approval. Follow the mainnet deployment process.

## Configuration

In `alembic/env.py`, configure:
- Import all models from `ledger_api.models.ledger_models`
- Set `target_metadata = Base.metadata`
- Configure database URL from environment variable

Example:
```python
from ledger_api.db import Base
from ledger_api.models import ledger_models

target_metadata = Base.metadata
```
