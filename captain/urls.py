from django.urls import path
from .views import CompleteCaptainProfileView

urlpatterns = [
    path('profile/complete/', CompleteCaptainProfileView.as_view(), name='complete-captain-profile'),
]
