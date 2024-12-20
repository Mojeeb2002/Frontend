from __future__ import with_statement
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base  # Adjust the import path to your project structure

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the database URL
DATABASE_URL = os.getenv("DATABASE_URL")


# Import your settings to get database configurations
from app.config import settings  # Adjust import path as needed

# This is the Alembic Config object, which provides access to the .ini file
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
# This will help Alembic to detect changes in your models
target_metadata = Base.metadata

# Build the database URL dynamically from the settings
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Set the SQLAlchemy URL for Alembic dynamically
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

# Define the engine with the new database URL
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create an engine using the dynamic URL
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Choose which mode to run migrations in (offline or online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
