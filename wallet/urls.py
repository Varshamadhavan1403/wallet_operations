from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
    )
from .views import (
    RegisterView, 
    WalletBalanceView, 
    WalletDepositView, 
    WalletWithdrawView, 
    TransactionHistoryView
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('wallet/balance/', WalletBalanceView.as_view(), name='wallet_balance'),
    path('wallet/deposit/', WalletDepositView.as_view(), name='wallet_deposit'),
    path('wallet/withdraw/', WalletWithdrawView.as_view(), name='wallet_withdraw'),
    path('wallet/history/', TransactionHistoryView.as_view(), name='transaction_history'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

