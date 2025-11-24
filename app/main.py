import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from time import time

from app.database.database import db
from app.database.settings import Base, engine

# ROUTES
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.verify_routes import router as verify_router

#  Logging
from app.utils.logging import app_logger


# LIFESPAN (Startup/Shutdown)
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


# INITIALIZE FASTAPI APP

app = FastAPI(
    title="User Management API with Auth, JWT, Roles & Email Verification",
    lifespan=lifespan
)

# ROOT
@app.get("/")
def root():
    app_logger.info("Root '/' endpoint accessed")
    return {"message": "Welcome to User Management API. Visit /docs"}


# INCLUDE ROUTERS

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(verify_router, prefix="/verify", tags=["Email Verification"])


# RUN SERVER

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
