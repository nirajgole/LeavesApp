from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine # Added create_engine
from alembic import context

# 1. IMPORT YOUR SETTINGS AND BASE
from app.core.config import settings
from app.db.base import Base  # This must import all models to register them

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. FIX TARGET METADATA
# Point this to your Base.metadata so Alembic can see your tables
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Pull the URL from your app settings instead of alembic.ini
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},

    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # 3. FIX ENGINE CREATION
    # We create the engine using your actual DATABASE_URL from .env
    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()