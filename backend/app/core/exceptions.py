from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    code: str
    request_id: str | None = None


class AgriSenseError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "agrisense_error"

    def __init__(self, detail: str):
        self.detail = detail


class NotFoundError(AgriSenseError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class ConflictError(AgriSenseError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


class ForbiddenError(AgriSenseError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden"


class UnauthorizedError(AgriSenseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AgriSenseError)
    async def handle_agrisense_error(request: Request, exc: AgriSenseError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                detail=exc.detail,
                code=exc.code,
                request_id=getattr(request.state, "request_id", None),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        request.app.state.logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                detail="An unexpected server error occurred.",
                code="internal_server_error",
                request_id=getattr(request.state, "request_id", None),
            ).model_dump(),
        )
