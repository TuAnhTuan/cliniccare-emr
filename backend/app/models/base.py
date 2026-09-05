from sqlalchemy.orm import declarative_base

# Shared declarative base — every model in this package must inherit from
# this exact object so they all register onto the same metadata/registry.
Base = declarative_base()
