from django.urls import path
from .views import CaptainProfileView, ClientProfileView

urlpatterns = [
    path('captain/profile/', CaptainProfileView.as_view(), name='captain-profile'),
    path('client/profile/', ClientProfileView.as_view(), name='client-profile'),
]
