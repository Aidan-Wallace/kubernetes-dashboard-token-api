import logging
from fastapi import APIRouter, Query, status
from fastapi.responses import HTMLResponse
from app.config import HTML_TEMPLATE
from app.models.health import HealthCheck
from app.models.token import BearerToken
from app.utils import get_token

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Serve HTML with the embedded bearer token",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
)
def get_bearer_token(redirect: bool = Query(default=True)):
    token = get_token()
    logger.info(f"Generated dashboard token: {token}")
    return HTML_TEMPLATE.replace("{TOKEN}", token).replace("{REDIRECT}", str(redirect))


@router.get(
    "/json",
    summary="Return the bearer token as a JSON",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=BearerToken,
)
def get_bearer_token_json():
    token = get_token()
    logger.info(f"Generated token as JSON: {token}")
    return BearerToken(token=token)


@router.get(
    "/text",
    response_class=HTMLResponse,
    summary="Return the bearer token as plain text",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
def get_bearer_token_string():
    token = get_token()
    logger.info(f"Generated token as text: {token}")
    return token


@router.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    logger.info("Health check was requested")
    return HealthCheck(status="OK")
