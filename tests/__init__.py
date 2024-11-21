import os

os.environ["HTML_FILE"] = "templates/index.html"
os.environ["KUBECTL_CMD"] = "/usr/local/bin/kubectl"
os.environ["KUBERNETES_DASHBOARD_URL"] = "https://k8s-dashboard.example.local"
os.environ["STATIC_DIRECTORY"] = "static"
