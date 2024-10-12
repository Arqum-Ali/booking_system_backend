# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('listings/create/', ListingCreateView.as_view(), name='listing-create'),
    # path('create-listing/', ListingCreateView.as_view(), name='create-listing'),
    path('listings/<int:pk>/', ListingCreateView.as_view(), name='listing-detail'),  # For retrieving a listing by ID
    path('listings/step2/create/', ListingCreateAPIView.as_view(), name='listing-create'),

]
