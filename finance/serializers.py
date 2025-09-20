from rest_framework import serializers
from .models import Category, Transaction
from django.db.models import Sum
from datetime import datetime, timedelta

class CategorySerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'total_amount']

    def get_total_amount(self, obj):
        total = obj.transactions.aggregate(sum=Sum('amount'))['sum']
        return total or 0

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'amount', 'comment', 'date']
        read_only_fields = ['user', ]

class DashboardSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
