from .authentication import authentication_routes
from .register import registry_routes
from .user import user_routes

__all__ = ['registry_routes', 'authentication_routes', 'user_routes']
