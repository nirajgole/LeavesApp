# Inside alembic/env.py
from app.db.base import Base
from app.core.config import settings

# 1. Set the metadata
target_metadata = Base.metadata

# 2. Set the URL from your settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)