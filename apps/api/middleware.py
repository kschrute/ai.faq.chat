"""
Custom middleware for input validation and security.
"""

import asyncio
import os
import time
from collections.abc import Callable

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers and input validation."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply security checks and headers."""

        # Input validation for POST requests
        if request.method == "POST":
            await self._validate_input(request)

        # Process the request
        response = await call_next(request)

        # Add security headers
        self._add_security_headers(response)

        return response

    async def _validate_input(self, request: Request) -> None:
        """Validate input for potential security issues."""
        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            return  # Let FastAPI handle content-type validation

        # Check content length
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                if int(content_length) > 10000:  # 10KB limit
                    return  # Let FastAPI handle large payload validation
            except ValueError:
                # Invalid content-length header, let FastAPI handle it
                return

    def _add_security_headers(self, response: Response) -> None:
        """Add security headers to response."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Only add CSP in production
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self'; "
                "img-src 'self' data:; "
                "connect-src 'self'"
            )

        # Add HSTS header only in production (assumes HTTPS)
        if os.getenv("ENVIRONMENT") == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Max calls per period
        self.period = period  # Period in seconds
        self.clients: dict[str, list[float]] = {}  # Simple in-memory storage
        self.last_cleanup = time.time()
        self._lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Apply rate limiting based on client IP."""
        client_ip = self._get_client_ip(request)
        current_time = time.time()

        async with self._lock:
            # Clean up old entries periodically
            if current_time - self.last_cleanup > 300:  # Every 5 minutes
                self._cleanup_old_entries(current_time)
                self.last_cleanup = current_time

            # Check rate limit
            if client_ip in self.clients:
                requests = self.clients[client_ip]

                # Count recent requests before appending
                recent_requests = [
                    req_time
                    for req_time in requests
                    if current_time - req_time <= self.period
                ]

                if len(recent_requests) >= self.calls:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")

                recent_requests.append(current_time)
                self.clients[client_ip] = recent_requests
            else:
                self.clients[client_ip] = [current_time]

        return await call_next(request)

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            try:
                return forwarded_for.split(",")[0].strip()
            except (AttributeError, IndexError):
                pass  # Fall back to other methods

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to client IP
        return request.client.host if request.client else "unknown"

    def _cleanup_old_entries(self, current_time: float) -> None:
        """Remove old entries from the rate limiting storage."""
        cutoff_time = current_time - self.period

        # Clean up each client's request history
        for client_ip in list(self.clients.keys()):
            requests = self.clients[client_ip]
            recent_requests = [
                req_time for req_time in requests if req_time > cutoff_time
            ]

            if not recent_requests:
                del self.clients[client_ip]
            else:
                self.clients[client_ip] = recent_requests
