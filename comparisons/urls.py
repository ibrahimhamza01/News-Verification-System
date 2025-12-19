from django.urls import path
from .views import handle_post_request  # Import your view class here

urlpatterns = [
    path('comparison-view/', handle_post_request, name='comparison-view'),
]
