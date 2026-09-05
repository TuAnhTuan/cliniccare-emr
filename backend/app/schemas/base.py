from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """Base for response schemas that serialize directly from SQLAlchemy model instances."""

    model_config = ConfigDict(from_attributes=True)
