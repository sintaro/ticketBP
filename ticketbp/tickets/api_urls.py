from rest_framework.routers import DefaultRouter

from . import api_views

ticket_router = DefaultRouter()

ticket_router.register(r'category', api_views.CategoryViewSet)
ticket_router.register(r'ticket', api_views.TicketViewSet)
ticket_router.register(r'freeticket', api_views.OnayamiTicketViewSet)
ticket_router.register(r'answer', api_views.AnswerViewSet)
ticket_router.register(r'review', api_views.AnswerReviewViewSet)