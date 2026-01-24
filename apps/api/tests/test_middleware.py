"""Tests for security and rate limiting middleware."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestSecurityMiddleware:
    """Test security middleware functionality."""

    def test_security_headers_present(self):
        """Test that security headers are added to responses."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert (
            response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        )

    def test_health_endpoint_works(self):
        """Test that health endpoint works with middleware."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_ready_endpoint_works(self):
        """Test that ready endpoint works with middleware."""
        response = client.get("/ready")
        # Should return 503 since engine isn't loaded in test client
        assert response.status_code in [200, 503]

    def test_metrics_endpoint_works(self):
        """Test that metrics endpoint works with middleware."""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "faq-chat"


class TestRateLimitMiddleware:
    """Test rate limiting middleware functionality."""

    def test_rate_limit_not_exceeded(self):
        """Test that normal usage doesn't trigger rate limiting."""
        # Make a few requests within the limit
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200

    def test_different_endpoints_work(self):
        """Test that different endpoints work with rate limiting."""
        endpoints = ["/health", "/metrics"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
