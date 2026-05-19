import logging
import traceback

from sqlalchemy import text

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.v1 import router as api_router
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.responses import error as error_response
from app.core.responses import success
from app.db.session import Base, engine
from app.middleware.registry import register_middlewares


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Mini Logistics OMS API",
        openapi_tags=[
            {
                "name": "orders",
                "description": "Order operations for customers",
            },
            {
                "name": "admin",
                "description": "Admin order operations",
            },
            {
                "name": "auth",
                "description": "Authentication endpoints",
            },
            {
                "name": "health",
                "description": "Health checks",
            },
        ],
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Swagger/OpenAPI JWT configuration
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        openapi_schema.setdefault(
            "components",
            {},
        ).setdefault(
            "securitySchemes",
            {},
        )

        openapi_schema["components"]["securitySchemes"][
            "bearerAuth"
        ] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }

        app.openapi_schema = openapi_schema

        return app.openapi_schema

    app.openapi = custom_openapi

    # Register API routes
    app.include_router(
        api_router,
        prefix="/api/v1",
    )

    # Register middleware
    register_middlewares(app)

    # Startup tasks
    @app.on_event("startup")
    async def startup():
        # Intentionally NOT running Base.metadata.create_all(bind=engine).
        # This avoids duplicate Oracle index creation during restarts.
        try:
            # Minimal DB connectivity verification
            with engine.connect() as conn:
                conn.execute(text("SELECT 1 FROM DUAL"))

            # Create Oracle sequences for auto-incrementing IDs
            from app.db.session import create_sequences
            create_sequences()

            logger.info(
                "Database connectivity check passed; schema creation skipped"
            )

        except Exception as exc:
            # Preserve startup resiliency
            logger.exception(
                f"Database connectivity check failed: {exc}"
            )

    # Centralized application exception handling
    @app.exception_handler(AppError)
    async def app_error_handler(
        request: Request,
        exc: AppError,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": str(exc.detail),
                "code": exc.status_code,
                "error_code": getattr(
                    exc,
                    "code",
                    "APP_ERROR",
                ),
            },
        )

    # Validation error normalization
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        errors = []

        for error in exc.errors():
            errors.append(
                {
                    "field": ".".join(
                        str(x)
                        for x in error["loc"][1:]
                    ),
                    "message": error["msg"],
                    "type": error["type"],
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "validation error",
                "code": 422,
                "error_code": "VALIDATION_ERROR",
                "details": errors,
            },
        )

    # Generic exception handler
    @app.exception_handler(Exception)
    async def generic_error_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            f"Unhandled application error: {str(exc)}"
        )

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(exc),
                "exception_type": exc.__class__.__name__,
                "code": 500,
                "error_code": "INTERNAL_ERROR",
            },
        )

    return app


app = create_app()


@app.get(
    "/healthz",
    tags=["health"],
    summary="Health check endpoint",
)
def health_check():
    return success(
        {
            "status": "ok",
            "service": settings.PROJECT_NAME,
        },
        message="service_healthy",
    )
