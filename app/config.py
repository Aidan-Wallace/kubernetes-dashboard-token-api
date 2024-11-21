import dotenv
import logging
import os

dotenv.load_dotenv()
logger = logging.getLogger("uvicorn.error")

HTML_FILE = os.environ.get("HTML_FILE", "templates/index.html")
KUBECTL_CMD = os.environ.get("KUBECTL_CMD")
KUBERNETES_DASHBOARD_URL = os.environ.get("KUBERNETES_DASHBOARD_URL")
STATIC_DIRECTORY = os.environ.get("STATIC_DIRECTORY", "static")

if KUBECTL_CMD is None:
    logger.error("Environment variable 'KUBECTL_CMD' is missing.")
    raise EnvironmentError("Cannot find env var 'KUBECTL_CMD'")

if not os.path.exists(HTML_FILE):
    raise FileNotFoundError(f"Cannot find file: '{HTML_FILE}'")

if not os.path.exists(STATIC_DIRECTORY):
    raise FileNotFoundError(f"Cannot find directory: '{STATIC_DIRECTORY}'")

with open(HTML_FILE, "r") as f:
    HTML_TEMPLATE = f.read()

if KUBERNETES_DASHBOARD_URL:
    HTML_TEMPLATE = HTML_TEMPLATE.replace(
        "{KUBERNETES_DASHBOARD_URL}",
        KUBERNETES_DASHBOARD_URL,
    )
