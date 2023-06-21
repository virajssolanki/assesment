from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from main.models import Transaction
from main.serializers import TransactionSerializer, CreateTansactionSerializer


class CreateTransactionView(generics.CreateAPIView):
    """
    this view is used to create a new transaction
    """
    serializer_class = CreateTansactionSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        method = getattr(Transaction, f'handle_{serializer.validated_data["trade_type"]}')
        if method:
            obj = method(
                qty = serializer.validated_data.get('qty', None),
                price = serializer.validated_data.get('price', None),
                date = serializer.validated_data.get('date', None),
                split_ratio = serializer.validated_data.get('split_ratio', None)
            )
            res_serializer = TransactionSerializer(obj)
            return Response(res_serializer.data, status=status.HTTP_201_CREATED)
