import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..database import get_db
from ..exceptions import UnauthorizedError
from ..models import Practitioner
from .tokens import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_practitioner(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Practitioner:
    try:
        practitioner_id = decode_access_token(token)
    except jwt.PyJWTError:
        raise UnauthorizedError("Invalid or expired token")

    practitioner = db.query(Practitioner).filter(Practitioner.id == practitioner_id).first()
    if practitioner is None:
        raise UnauthorizedError("Invalid or expired token")
    return practitioner
