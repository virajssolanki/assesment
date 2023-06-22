from django.contrib import admin
from django.urls import path

from main.apis import CreateTransactionView, GetHoldingView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/transaction/', CreateTransactionView.as_view(), name='create-transaction'),
    path('api/holding/<str:date>/', GetHoldingView.as_view(), name='get-holding'),
]
