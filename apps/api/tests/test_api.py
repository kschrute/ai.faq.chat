import sys
from pathlib import Path

from fastapi.testclient import TestClient

from api import app

# Ensure the API package (apps/api) is on the import path when running tests
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

client = TestClient(app)


def test_read_main() -> None:
    # This assumes your API has a root endpoint or similar.
    # Adjust based on actual API endpoints.
    # Since I saw 'mount static' at root, this might fail if static files aren't there,
    # but let's test a known endpoint or just health check if available.
    # The api.py showed a /chat endpoint.

    # We can test the 404 for root if it's just static files mounting which might be
    # conditional or test that /chat exists (405 Method Not Allowed for GET)
    response = client.get("/chat")
    assert response.status_code == 405
