from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category,Answer,Ticket,OnayamiTicket,AnswerReview

class UserSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
    	model = User

        fields = ('id', 'uuid', 'username', 'full_name',
          'email', 'departments', 'is_bussiness_account','is_active','date_joined')

class  CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category

		fields = ('name','extra_fee_rate','display_priority')

class AnswerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Answer

		fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Ticket

		fields = '__all__'

class OnayamiTicketSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = OnayamiTicket

		fields = '__all__'

class AnswerReviewSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = AnswerReview

		fields = '__all__'
