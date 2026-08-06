from fastapi import FastAPI
from app.api.routes import router
from app.api.dashboard import router as dashboard_router
app = FastAPI(
    title="AI Traffic Analysis System",
    version="1.0.0",
    description="Backend API for Intelligent Traffic Monitoring"
)

app.include_router(router)
app.include_router(dashboard_router)