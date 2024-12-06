from src.api.user import api_router as auth_router
from src.api.legal_entity import api_router as legal_entity_router
from src.api.feedback import api_router as feedback_router
from src.api.payments import api_router as payment_router
from src.api.ping import api_router as ping_router


list_of_routes = [
    legal_entity_router,
    auth_router,
    feedback_router,
    payment_router,
    ping_router,
]


__all__ = ["list_of_routes"]
