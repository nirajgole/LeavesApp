from fastapi import FastAPI
from app.api.v1.endpoints import auth, leaves, dashboard, employees
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# This command creates all tables in the database if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Account endpoints (Authentication)
app.include_router(auth.router, prefix="/api/v1.0/Account", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/v1.0/Employee", tags=["Employee"])

# HR Module endpoints [cite: 52]
app.include_router(leaves.router, prefix="/api/v1.0", tags=["Leave Management"])

app.include_router(
    dashboard.router,
    prefix="/api/v1.0/Dashboard",
    tags=["HR Dashboard"]
)

@app.get("/")
def root():
    return {"message": "HR Module API is running", "docs": "/docs"}

