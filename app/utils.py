import logging
import subprocess
from app.config import KUBECTL_CMD

logger = logging.getLogger("uvicorn.error")


def get_token():
    """
    Executes the kubectl command to create a token for the Kubernetes dashboard.
    """
    cmd = f"{KUBECTL_CMD} -n kubernetes-dashboard create token admin-user"

    try:
        result = subprocess.check_output(cmd.split()).decode("utf-8").strip()

        return result
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise
