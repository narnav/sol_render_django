import datetime
from django.http import JsonResponse
from .models import Trips, Expenses, CurrencyRate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ExpensesSerializer,TripsSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import requests

from django.core.mail import get_connection, send_mail
from django.conf import settings




@api_view(['GET','post'])
def test(request):
    connection = get_connection()
    connection.open()
    send_mail(
    "waga say hello",
    "waga is the message.",
    settings.EMAIL_HOST_USER,
    ["soli0003@gmail.com"],
    fail_silently=False,
    )
    connection.close()
    return Response("email sent")





# ---------------------------------------------------------------------------- login and register  -----------------------------------------------------------------------------------------#




# register
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Instantiate the EmailValidator
    email_validator = EmailValidator()

    try:
        email_validator(email)  # Validate email format
    except ValidationError:
        return Response({"message": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)
    # Check password length
    if len(password) < 8:
        return Response({"message": "Password too short"}, status=status.HTTP_400_BAD_REQUEST) 

    # Create a new user
    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)







 
 #login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ----------------------------------------------------------------------------------------------------- CRUD ----------------------------------------------------------------------------------------------------------#

class ExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trips=None):
        user = request.user
        if trips:
            expenses = Expenses.objects.filter(user=user, trips__description=trips)
        else:
            expenses = Expenses.objects.filter(user=user)
        serializer = ExpensesSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpensesSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        expense = Expenses.objects.get(pk=pk)
        if expense.user == request.user:
            serializer = ExpensesSerializer(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You do not have permission to update this expense."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        expense = Expenses.objects.get(pk=pk)
        if expense.user == request.user:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You do not have permission to delete this expense."}, status=status.HTTP_403_FORBIDDEN)
    
    
# ----------------------------------------------------------------------------------------------------- Get & Add Trips ----------------------------------------------------------------------------------------------------------#

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTrips(request):
    user = request.user
    trips = Trips.objects.filter(user=user)
    serializer = TripsSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTrips(request):
    serializer = TripsSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ----------------------------------------------------------------------------------------------------- Get Currency Rate ----------------------------------------------------------------------------------------------------------#

def fetch_currency_rates(request):
    url = "https://exchange-rate-api1.p.rapidapi.com/latest"
    querystring = {"base": "USD"}
    headers = {
        "X-RapidAPI-Key": "789f7dfa02mshef0ff2d3beee502p1c84bfjsnc19c4875fbe3",
        "X-RapidAPI-Host": "exchange-rate-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if response.status_code == 200:
        base_currency = data["base"]
        time_utc_str = data["time_update"]["time_utc"]
        time_utc = datetime.datetime.strptime(time_utc_str, "%Y-%m-%dT%H:%M:%SZ")

        for target_currency, exchange_rate in data["rates"].items():
            # Create a CurrencyRate object and save it to the database
            rate = CurrencyRate(
                base_currency=base_currency,
                target_currency=target_currency,
                exchange_rate=exchange_rate,
                time_utc=time_utc
            )
            rate.save()

        return JsonResponse({"message": "Currency data fetched and stored successfully."})
    else:
        return JsonResponse({"message": "Failed to fetch currency data."})

