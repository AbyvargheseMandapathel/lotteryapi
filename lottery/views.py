from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lottery.permissions import IsStaffUser
from .models import Lottery
from .serializers import LotteryListSerializer, LotterySerializer


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return LotteryListSerializer  # Minimal fields for list
        return LotterySerializer  # Full serializer for retrieve, create, update


class LotteryUploadView(APIView):
    
    permission_classes = [IsStaffUser]
    
    def post(self, request, *args, **kwargs):
        serializer = LotterySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Lottery saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LotteryResultDetailAPIView(APIView):
    """
    Get lottery details by ID.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            lottery = Lottery.objects.prefetch_related(
                "prizes__winning_tickets", "prizes__consolation_prize"
            ).get(pk=pk)
            serializer = LotterySerializer(lottery)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Lottery.DoesNotExist:
            return Response({"error": "Lottery not found"}, status=status.HTTP_404_NOT_FOUND)
