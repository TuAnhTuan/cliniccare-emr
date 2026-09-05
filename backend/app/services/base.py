from sqlalchemy.orm import Session


class BaseService:
    """Base for services that need a DB session to query/persist data."""

    def __init__(self, db: Session):
        self.db = db
