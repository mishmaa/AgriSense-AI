from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware, SecurityHeadersMiddleware
from app.db.base import Base
from app.db.session import engine
from app.websocket.routes import router as websocket_router

# Import all models so SQLAlchemy can register metadata before create_all/Alembic.
import app.models  # noqa: F401, E402


settings = get_settings()
logger = configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name,
        version="0.1.0",
        default_response_class=JSONResponse,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    )
    app.state.logger = logger

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=settings.gzip_minimum_size)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.trusted_hosts)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.include_router(websocket_router)

    @app.on_event("startup")
    def startup() -> None:
        if not settings.is_production:
            Base.metadata.create_all(bind=engine)
        logger.info("AgriSense AI backend started environment=%s", settings.environment)

    @app.get("/health", tags=["System"])
    def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.project_name}

    return app


app = create_app()
