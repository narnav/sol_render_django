from . import views
from django.urls import path
from .views import ExpensesView, TokenObtainPairView
from rest_framework_simplejwt.views import ( TokenRefreshView)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('addTrips', views.addTrips),
    path('test', views.test),
    path('getTrips', views.getTrips),
    path('getRates/', views.fetch_currency_rates, name='get-rates'),
    path('expenses', ExpensesView.as_view()),
    path('expenses/<int:pk>', ExpensesView.as_view()),
    path('expenses/<str:trips>', ExpensesView.as_view(), name='expenses_by_trips'),
    path('expenses/trips/<str:trips>/', views.ExpensesView.as_view(), name='expenses_by_trips'),
    path('login', views.MyTokenObtainPairView.as_view()),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh', TokenRefreshView.as_view()),
    path('register', views.register),
]