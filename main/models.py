from django.db import models


class Transaction(models.Model):
    """
    This table will store all the transactions done by the investor.
    After each transaction:
    - the avg_buy_price and balance_qty will be updated
    - so to get these values, we need to query the table for latest transaction
    - split transaction will add a new buy transaction with same date as original transaction
    for simplicity, we are asuming that all transaction are for single company only and FK to investor is not added
    """
    class TRADE_TYPE(models.TextChoices):
        BUY = 'BUY'
        SELL = 'SELL'
        SPLIT = 'SPLIT'
    
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(null=False, blank=False, default=None)
    trade_type = models.CharField(max_length=5, choices=TRADE_TYPE.choices)
    qty = models.IntegerField(null=True, blank=True)
    balance_qty = models.IntegerField(null=True, blank=True)
    #balance qty == qty while buying then on selling it will be reduced

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    split_ratio = models.IntegerField(default=None, null=True, blank=True)
    
    avg_buy_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_holding_qty = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.date} - {self.trade_type} - {self.qty} - {self.price}'
     
    
    @classmethod
    def handle_BUY(cls, qty, price, date, split_ratio=None):
        """
        This method will handle BUY transaction
        """
        avg_buy_price = price
        total_holding_qty = qty
        last_transaction = cls.objects.order_by('-timestamp').first()
        
        if last_transaction:
            total_holding_qty = last_transaction.total_holding_qty + qty
            avg_buy_price = ((last_transaction.avg_buy_price * last_transaction.total_holding_qty + qty * price) 
                / total_holding_qty)

        return cls.objects.create(
            trade_type=cls.TRADE_TYPE.BUY,
            date=date,
            qty=qty,
            balance_qty=qty,
            price=price,
            avg_buy_price=avg_buy_price,
            total_holding_qty = total_holding_qty
        )
        
        
    @classmethod
    def handle_SELL(cls, qty, price, date, split_ratio=None):
        """
        This method will handle SELL transaction
        """
        # import pdb
        # pdb.set_trace()
        
        selling_qty = qty
        transactions_query = cls.objects.filter(balance_qty__gt=0, trade_type="BUY").order_by('timestamp')
        last_transaction = transactions_query.last()
        if last_transaction.total_holding_qty < qty:
            raise Exception('Not enough balance quantity')
        
        last_total_holding_qty = last_transaction.total_holding_qty
        avg_buy_price = last_transaction.avg_buy_price
        
        for transaction in transactions_query.all():
            if transaction.balance_qty >= selling_qty:
                transaction.balance_qty = transaction.balance_qty - selling_qty
                transaction.save()

                avg_buy_price = ((avg_buy_price * last_total_holding_qty - selling_qty * transaction.price) 
                 / (last_total_holding_qty - selling_qty))
                last_total_holding_qty = last_total_holding_qty - selling_qty
                break
            
            else:
                selling_qty = selling_qty - transaction.balance_qty
                transaction.balance_qty = 0                
                transaction.save()
                
                avg_buy_price = ((avg_buy_price * last_total_holding_qty - transaction.qty * transaction.price) 
                / (last_total_holding_qty - transaction.qty))
                last_total_holding_qty = last_total_holding_qty - transaction.qty
                
        return cls.objects.create(
            trade_type=cls.TRADE_TYPE.SELL,
            qty=qty,
            price=price,
            avg_buy_price=avg_buy_price,
            total_holding_qty=last_total_holding_qty,
            balance_qty=qty,
            date=date,
        )
            
            
    @classmethod
    def handle_SPLIT(cls, split_ratio, date=None, qty=None, price=None):
        """
        This method will handle SPLIT transaction
        split ratio is integer value for 1:2 split ratio, split_ratio=2
        """
        transactions = cls.objects.filter(
            balance_qty__gt=0,
            trade_type__in=["BUY", "SELL"]
        ).order_by('timestamp')
        
        if not transactions:
            return cls.objects.create(
                trade_type=cls.TRADE_TYPE.SPLIT,
                split_ratio=split_ratio,                
            )
            
        for transaction in transactions:
            cls.objects.create(
                date=transaction.date,
                trade_type=transaction.trade_type,
                qty=transaction.qty * split_ratio,
                balance_qty=transaction.balance_qty * split_ratio,
                price=transaction.price / split_ratio,
                avg_buy_price=transaction.avg_buy_price / split_ratio,
                total_holding_qty=transaction.total_holding_qty * split_ratio,
            )
            transaction.balance_qty = 0
            transaction.save()
        
        return cls.objects.create(
            date= transactions.last().date,
            trade_type=cls.TRADE_TYPE.SPLIT,
            split_ratio=split_ratio,
            avg_buy_price=transactions.last().avg_buy_price,
            total_holding_qty=transactions.last().total_holding_qty,
        )

                
                