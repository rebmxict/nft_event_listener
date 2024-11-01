from django.urls import path
from .views import transfer_history

urlpatterns = [
    path('history/<str:token_id>/', transfer_history, name='transfer-history'),
]
