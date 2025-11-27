import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import traceback

from fastapi.openapi.utils import get_openapi

from app.database.database import db
from app.database.settings import Base, engine

# ROUTES
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.verify_routes import router as verify_router
from app.routes.note_routes import router as note_router
# Logging
from app.utils.logging import app_logger


# -------------------- LIFESPAN --------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events cleanly."""
    try:
        # ---- STARTUP ----
        Base.metadata.create_all(bind=engine)
        db.connect()
        app_logger.info("Application startup complete.")
        yield
    finally:
        # ---- SHUTDOWN ----
        db.disconnect()
        app_logger.info("Application shutdown complete.")

app = FastAPI(
    title="User Management API",
    description="User Management API with Authentication, JWT, Roles & Admin Controls",
    version="1.0.0",
    lifespan=lifespan
)


# -------------------- SWAGGER SECURITY --------------------

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add Bearer Token Auth
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    app_logger.error(
        f"Unhandled Error: {exc}\n"
        f"Path: {request.url}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    app_logger.warning(
        f"HTTP Error {exc.status_code} at {request.url}: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    app_logger.warning(f"Validation Error at {request.url}: {exc.errors()}")

    clean = []
    for err in exc.errors():
        clean.append({
            "loc": err.get("loc"),
            "msg": err.get("msg"),
            "type": err.get("type")
        })

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid input",
            "errors": clean
        }
    )


@app.get("/")
def root():
    return {"message": "Welcome to User Management API — open /docs for Swagger UI"}


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(verify_router, prefix="/verify", tags=["Email Verification"])
app.include_router(note_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
