from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import (
    status, 
    generics
    )
from decimal import Decimal 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Wallet, Transaction
from .serializers import (
    UserSerializer, 
    WalletSerializer, 
    TransactionSerializer)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wallet = request.user.wallet
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)


class WalletDepositView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        amount = request.data.get('amount')
        if amount is None:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValidationError("Amount must be positive")
        except (ValueError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = request.user.wallet
            wallet.balance += amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='DEPOSIT',
                description='Deposit to wallet'
            )

            return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletWithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        amount = request.data.get('amount')
        if amount is None:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValidationError("Amount must be positive")
        except (ValueError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = request.user.wallet
            if wallet.balance < amount:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            
            wallet.balance -= amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='WITHDRAWAL',
                description='Withdrawal from wallet'
            )

            return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletWithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get('amount')
            
            # Convert amount to Decimal
            amount_decimal = Decimal(amount)
            
            wallet = request.user.wallet
            
            # Check if the user has sufficient balance for the withdrawal
            if wallet.balance < amount_decimal:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update wallet balance using Decimal arithmetic
            wallet.balance -= amount_decimal
            wallet.save()
            
            # Create a transaction record for the withdrawal with transaction_type as "withdrawal"
            transaction = Transaction.objects.create(wallet=wallet, amount=amount_decimal, transaction_type='withdrawal')
            
            # Serialize the transaction
            transaction_serializer = TransactionSerializer(transaction)
            
            # Include balance in response data
            response_data = {
                "transaction": transaction_serializer.data,
                "balance": str(wallet.balance),
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve all transactions for the authenticated user's wallet
            transactions = Transaction.objects.filter(wallet__user=request.user)
            
            # Check if transactions exist
            if not transactions:
                return Response({"message": "No transactions found"}, status=status.HTTP_204_NO_CONTENT)
            
            # Serialize transaction data
            serializer = TransactionSerializer(transactions, many=True)
            
            # Calculate current wallet balance
            current_balance = request.user.wallet.balance
            
            # Construct response data
            response_data = {
                "history": serializer.data,
                "balance": str(current_balance),
            }
            
            # Return transaction history with balance in the response
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
