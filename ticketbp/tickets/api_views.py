from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Category,Answer,Ticket,OnayamiTicket,AnswerReview
from .serializers import UserSerializer,CategorySerializer,AnswerSerializer,TicketSerializer,OnayamiTicketSerializer,AnswerReviewSerializer


class CategoryViewSet(ReadOnlyModelViewSet):

	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class AnswerViewSet(ReadOnlyModelViewSet):

	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

class TicketViewSet(ReadOnlyModelViewSet):

	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer

class OnayamiTicketViewSet(ReadOnlyModelViewSet):

	queryset = OnayamiTicket.objects.all()
	serializer_class = OnayamiTicketSerializer

class AnswerReviewViewSet(ReadOnlyModelViewSet):

	queryset = AnswerReview.objects.all()
	serializer_class = AnswerReviewSerializer
