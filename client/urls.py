from django.urls import path
from .views import CompleteClientProfileView

urlpatterns = [
    path('profile/complete/', CompleteClientProfileView.as_view(), name='complete-client-profile'),
]
