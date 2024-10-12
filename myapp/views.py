# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import ListingCreateSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Listing
from .serializers import ListingSerializer

class ListingCreateView(APIView):
    def post(self, request):
        serializer = ListingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# views.py
    def get(self, request, pk):
        try:
            listing = Listing.objects.get(pk=pk)  # Fetch listing by primary key (ID)
            serializer = ListingCreateSerializer(listing)  # Use your existing serializer
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class ListingCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = ListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
