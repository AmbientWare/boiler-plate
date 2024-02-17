import os
from fastapi import APIRouter
from loguru import logger
from fastapi.responses import FileResponse

# project imports
from app.core.config import FRONTEND_BUILD_DIR

main_router = r = APIRouter()


@r.get("/{path_name:path}")
async def serve(path_name: str):
    static_folder = FRONTEND_BUILD_DIR
    # Check if the requested path exists in static files
    if path_name and os.path.exists(os.path.join(static_folder, path_name)):
        return FileResponse(os.path.join(static_folder, path_name))
    else:
        # Serve index.html by default
        return FileResponse(os.path.join(static_folder, "index.html"))
