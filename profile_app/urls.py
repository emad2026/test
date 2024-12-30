from django.urls import path
from .views import ClientProfileAPIView

urlpatterns = [
    path('client-profiles/', ClientProfileAPIView.as_view(), name='client-profiles'),
]
