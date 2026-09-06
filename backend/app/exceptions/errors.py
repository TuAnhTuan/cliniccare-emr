from fastapi import status


class AppError(Exception):
    """Base class for application errors that map to a specific HTTP response."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad request"
