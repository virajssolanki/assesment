from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from main.models import Transaction
from main.serializers import TransactionSerializer, CreateTansactionSerializer, HoldingViewSerializer

from datetime import datetime


class CreateTransactionView(generics.CreateAPIView):
    """
    this view is used to create a new transaction
    """
    serializer_class = CreateTansactionSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """

        url: http://127.0.0.1:8000/api/transaction/
        sample payload for buy transaction:{
            "trade_type": "BUY",
            "qty": 100,
            "price": 200,
            "split_ratio": null,
            "date": "2023-06-20"
        }
        sample payload for split transaction:{
            "trade_type": "SPLIT",
            "qty": null,
            "price": null,
            "split_ratio": 2,
            "date": "2023-06-20"
        }
        """
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



class GetHoldingView(generics.RetrieveAPIView):
    """
    this view is used to get the holding details
    pass date in YYYY-MM-DD as path parameter

    sample url 
    http://127.0.0.1:8000/api/holding/2023-06-16/
    """
    serializer_class = HoldingViewSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        try:
            date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError(detail="Invalid date format. Please use 'YYYY-MM-DD'.")

        transaction = Transaction.objects.filter(date__lte=date).order_by('-timestamp').first()
        print(transaction)
        if not transaction:
            raise NotFound(detail="No transaction found for the given date.")
        return transaction