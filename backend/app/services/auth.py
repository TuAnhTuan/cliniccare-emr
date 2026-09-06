from datetime import datetime, timezone

from ..exceptions import UnauthorizedError
from ..models import Practitioner, RefreshToken
from ..security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    verify_password,
)
from .base import BaseService


class AuthService(BaseService):
    def login(self, email: str, password: str) -> tuple[str, str]:
        practitioner = self.db.query(Practitioner).filter(Practitioner.email == email).first()
        if practitioner is None or not practitioner.hashed_password:
            raise UnauthorizedError("Invalid email or password")
        if not verify_password(password, practitioner.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        return self._issue_tokens(practitioner.id)

    def refresh(self, raw_refresh_token: str) -> tuple[str, str]:
        token_hash = hash_refresh_token(raw_refresh_token)
        stored = self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

        # expires_at is stored naive (assumed UTC), so compare against a naive UTC "now".
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        if stored is None or stored.revoked or stored.expires_at < now_utc:
            raise UnauthorizedError("Invalid or expired refresh token")

        # Rotate: the presented refresh token is single-use. Revoking it here means
        stored.revoked = True
        self.db.flush()

        return self._issue_tokens(stored.practitioner_id)

    def logout(self, raw_refresh_token: str) -> None:
        token_hash = hash_refresh_token(raw_refresh_token)
        stored = self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        if stored is not None:
            stored.revoked = True
        self.db.commit()

    def _issue_tokens(self, practitioner_id: int) -> tuple[str, str]:
        access_token = create_access_token(practitioner_id)
        raw_refresh_token, token_hash, expires_at = generate_refresh_token()
        self.db.add(
            RefreshToken(
                practitioner_id=practitioner_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
        )
        self.db.commit()
        return access_token, raw_refresh_token
