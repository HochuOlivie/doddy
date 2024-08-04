from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('increase-balance/', views.IncreaseBalanceView.as_view(), name='increase-balance'),
    path('farms', views.FarmsView.as_view(), name='farms'),
    path('buy-farm/', views.BuyFarmView.as_view(), name='buy-farm'),
]