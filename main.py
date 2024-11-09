import logging
import dotenv
import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

HTML_FILE = "index.html"
KUBERNETES_DASHBOARD_URL_KEY = "KUBERNETES_DASHBOARD_URL"
KUBECTL_CMD_KEY = "KUBECTL_CMD"

dotenv.load_dotenv()

logger = logging.getLogger("uvicorn.error")

kubernetes_dashboard_url = os.getenv("KUBERNETES_DASHBOARD_URL")
kubectl_cmd = os.getenv(KUBECTL_CMD_KEY)

if kubectl_cmd is None:
    logger.error(f"find env var '{KUBECTL_CMD_KEY}'")
    raise EnvironmentError(f"Cannot find env var '{KUBECTL_CMD_KEY}'")

logger.info(f"found '{kubernetes_dashboard_url}' as dashboard url")
logger.info(f"found '{kubectl_cmd}' as kubectl command")

if not os.path.exists(HTML_FILE):
    raise FileNotFoundError(f"Cannot find file: '{HTML_FILE}'")

with open(HTML_FILE, "r") as f:
    html = f.read()

if kubernetes_dashboard_url is not None:
    html = html.replace("{KUBERNETES_DASHBOARD_URL}", kubernetes_dashboard_url)

app = FastAPI()


def get_token():
    cmd = f"{kubectl_cmd} -n kubernetes-dashboard create token admin-user"
    result = subprocess.check_output(cmd.split(" ")).decode("utf-8")
    return result


@app.get("/", response_class=HTMLResponse)
def get_bearer_token():
    result = get_token()
    logger.info(f"received request to get dashboard token. token: {result}")
    return html.replace("{TOKEN}", result)


@app.get("/json")
def get_bearer_token_json():
    result = get_token()
    logger.info(f"received request to get dashboard token. token: {result}")
    return {"result": result}
