import logging
import os

import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from fastapi import FastAPI

from mock_copilotkit_server.config import config
from mock_copilotkit_server.service.copilot_service import (
    copilotkit_sdk,
    test_copilotkit_actions,
)

# Configure logging
logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(debug=config.debug)


# Add a health check endpoint
@app.get("/health")
async def health_check():
    logger.info("🏥 [HEALTH CHECK] Health check endpoint called")
    return {"status": "healthy", "message": "CopilotKit server is running"}


# Add a test endpoint to verify server is running
@app.get("/")
async def root():
    logger.info("🌐 [ROOT] Root endpoint called")
    return {
        "message": "CopilotKit Server is running",
        "actions": len(copilotkit_sdk.actions),
    }


# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, copilotkit_sdk, "/copilotkit_remote")


# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📨 [REQUEST] {request.method} {request.url.path} " f"- Headers: {dict(request.headers)}")

    response = await call_next(request)
    logger.info(f"📤 [RESPONSE] {response.status_code} for {request.url.path}")
    return response


def main():
    """Run the uvicorn server."""
    logger.info("🚀 [SERVER] Starting CopilotKit server...")
    logger.info(f"📊 [SERVER] Registered {len(copilotkit_sdk.actions)} actions:")
    for action in copilotkit_sdk.actions:
        logger.info(f"  - {action.name}: {action.description}")

    port = int(os.environ.get("PORT", 8000))
    logger.info("🌍 [SERVER] Server will be available at:")
    logger.info(f"  - http://0.0.0.0:{port} - API documentation")
    logger.info(f"  - http://0.0.0.0:{port}/health - Health check")
    logger.info(f"  - http://0.0.0.0:{port}/copilotkit_remote - CopilotKit endpoint")

    # Test actions
    test_copilotkit_actions()

    uvicorn.run(
        "server:app",
        host=config.server_host,
        port=config.server_port,
        reload=config.server_reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
