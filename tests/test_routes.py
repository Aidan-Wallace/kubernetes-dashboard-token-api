import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestRoutes:
    client = TestClient(app)

    def test_get_bearer_token(self):
        response = self.client.get("/")

        assert response.status_code == 200
        assert "mocked-token" in response.text
        assert "https://" in response.text

    def test_get_bearer_token_favicon(self):
        response = self.client.get("/static/favicon.png")

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_get_bearer_token_json(self):
        response = self.client.get("/json")

        assert response.status_code == 200
        assert response.json() == {"token": "mocked-token"}

    def test_get_bearer_token_string(self):
        response = self.client.get("/text")

        assert response.status_code == 200
        assert response.text == "mocked-token"

    def test_get_health(self):
        response = self.client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

    @pytest.fixture(autouse=True)
    def set_env_vars(self, monkeypatch: pytest.MonkeyPatch):
        # Note: This isn't working as expected. all environment
        # variables used are set in `__init__.py`.

        monkeypatch.setenv("HTML_FILE", "templates/index.html")
        monkeypatch.setenv("KUBECTL_CMD", "/usr/local/bin/kubectl")
        monkeypatch.setenv(
            "KUBERNETES_DASHBOARD_URL",
            "https://k8s-dashboard.example.local",
        )
        monkeypatch.setenv("STATIC_DIRECTORY", "static")

    @pytest.fixture(autouse=True)
    def mock_get_token(self, monkeypatch: pytest.MonkeyPatch):
        def fake_get_token():
            return "mocked-token"

        monkeypatch.setattr("app.router.routes.get_token", fake_get_token)
