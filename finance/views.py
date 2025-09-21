from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer, DashboardSerializer

class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Transaction, pk=pk, user=user)

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        categories = Category.objects.filter(user=user)
        data = []

        for cat in categories:
            total = cat.transactions.aggregate(sum=Sum('amount'))['sum'] or 0
            data.append({
                'category_name': cat.name,
                'type': cat.type,
                'total': total
            })

        income = transactions.filter(category__type='income').aggregate(sum=Sum('amount'))['sum'] or 0
        expense = transactions.filter(category__type='expense').aggregate(sum=Sum('amount'))['sum'] or 0
        balance = income - expense

        return Response({
            'balance': balance,
            'categories': data
        }, status=status.HTTP_200_OK)



class SummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, period, *args, **kwargs):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            start = parse_date(start_date_str)
            end = parse_date(end_date_str)
            if not start or not end:
                return Response({'error': 'Invalid date format, use YYYY-MM-DD'},
                                status=status.HTTP_400_BAD_REQUEST)
            end = datetime.combine(end, datetime.max.time())
        else:
            now = datetime.now()
            if period == 'daily':
                start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'weekly':
                start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'monthly':
                start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                return Response({'error': 'Invalid period'}, status=status.HTTP_400_BAD_REQUEST)
            end = now

        filtered = transactions.filter(date__gte=start, date__lte=end)
        income = filtered.filter(category__type='income').aggregate(sum=Sum('amount'))['sum'] or 0
        expense = filtered.filter(category__type='expense').aggregate(sum=Sum('amount'))['sum'] or 0
        balance = income - expense

        return Response({
            'start_date': start.date(),
            'end_date': end.date(),
            'income': income,
            'expense': expense,
            'balance': balance
        }, status=status.HTTP_200_OK)
