"""
Domain-specific exceptions for the application.
"""


class ServiceError(Exception):
    """Base class for service-level errors."""

    pass


class ServiceNotReadyError(ServiceError):
    """Raised when the service dependencies (model, index) are not fully initialized."""

    pass


class ModelError(ServiceError):
    """Raised when there is an error with the ML model."""

    pass


class InvalidInputError(ServiceError):
    """Raised when input validation fails in the business logic."""

    pass
