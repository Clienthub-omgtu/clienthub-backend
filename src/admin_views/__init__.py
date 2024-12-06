from .legal_entity import LegalEntityView
from .user import UserView
from .payments import PaymentView
from .feedback_about_client import FeedBackAboutClientsView


list_of_views = [LegalEntityView, UserView, PaymentView, FeedBackAboutClientsView]


__all__ = ["list_of_views"]
