import logging
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from app.config import HTML_TEMPLATE
from app.utils import get_token

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def get_bearer_token(redirect: bool = Query(default=True)):
    """
    Serve HTML with the embedded bearer token.
    """
    token = get_token()
    logger.info(f"Generated dashboard token: {token}")
    return HTML_TEMPLATE.replace("{TOKEN}", token).replace("{REDIRECT}", str(redirect))


@router.get("/json")
def get_bearer_token_json():
    """
    Return the bearer token as a JSON response.
    """
    token = get_token()
    logger.info(f"Generated token as JSON: {token}")
    return {"result": token}


@router.get("/text", response_class=HTMLResponse)
def get_bearer_token_string():
    """
    Return the bearer token as plain text.
    """
    token = get_token()
    logger.info(f"Generated token as text: {token}")
    return token
