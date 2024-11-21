import logging
import dotenv
import os
import subprocess
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

HTML_FILE = "HTML_FILE"
KUBECTL_CMD_KEY = "KUBECTL_CMD"
KUBERNETES_DASHBOARD_URL_KEY = "KUBERNETES_DASHBOARD_URL"
STATIC_DIRECTORY = "STATIC_DIRECTORY"

dotenv.load_dotenv()

logger = logging.getLogger("uvicorn.error")

html_file = os.environ.get(HTML_FILE, "templates/index.html")
kubectl_cmd = os.environ.get(KUBECTL_CMD_KEY)
kubernetes_dashboard_url = os.environ.get("KUBERNETES_DASHBOARD_URL")
static_directory = os.environ.get(STATIC_DIRECTORY, "static")

logger.info(f"found '{html_file}' as html file")
logger.info(f"found '{kubectl_cmd}' as kubectl command")
logger.info(f"found '{kubernetes_dashboard_url}' as dashboard url")
logger.info(f"found '{static_directory}' as static data directory")

if kubectl_cmd is None:
    logger.error(f"find env var '{KUBECTL_CMD_KEY}'")
    raise EnvironmentError(f"Cannot find env var '{KUBECTL_CMD_KEY}'")
if not os.path.exists(html_file):
    raise FileNotFoundError(f"Cannot find file: '{html_file}'")
if not os.path.exists(static_directory):
    raise FileNotFoundError(f"Cannot find directory: '{static_directory}'")

with open(html_file, "r") as f:
    html = f.read()

if kubernetes_dashboard_url is not None:
    html = html.replace("{KUBERNETES_DASHBOARD_URL}", kubernetes_dashboard_url)

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_directory), name=static_directory)


def get_token():
    cmd = f"{kubectl_cmd} -n kubernetes-dashboard create token admin-user"
    result = subprocess.check_output(cmd.split(" ")).decode("utf-8")
    return result


@app.get("/", response_class=HTMLResponse)
def get_bearer_token(redirect: bool = Query(default=True)):
    result = get_token()
    logger.info(f"received request to get dashboard token from webui. token: {result}")

    return html.replace("{TOKEN}", result).replace("{REDIRECT}", str(redirect))


@app.get("/json")
def get_bearer_token_json():
    result = get_token()
    logger.info(f"received request to get dashboard token as json. token: {result}")
    return {"result": result}


@app.get("/text", response_class=HTMLResponse)
def get_bearer_token_string():
    result = get_token()
    logger.info(f"received request to get dashboard token as string. token: {result}")
    return result
