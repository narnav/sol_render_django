from rest_framework import serializers
from .models import Expenses, Trips
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        

class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
 
        return token