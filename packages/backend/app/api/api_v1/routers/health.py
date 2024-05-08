from fastapi import APIRouter

health_routers = r = APIRouter()


# health check route
@r.get("/health")
async def health_check():
    """Check the health of the API."""
    return {"status": "ok"}
