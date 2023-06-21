from django.contrib import admin
from django.urls import path

from main.apis import CreateTransactionView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/transaction/', CreateTransactionView.as_view(), name='create-transaction'),
    
]
