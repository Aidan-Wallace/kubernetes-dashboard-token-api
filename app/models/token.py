from pydantic import BaseModel


class BearerToken(BaseModel):
    """Response model to return a bearer token"""

    token: str = "OK"
