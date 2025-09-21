from django.urls import path
from .views import (CategoryListCreateAPIView,TransactionAPIView,TransactionDetailAPIView,
    DashboardAPIView,SummaryAPIView,)

urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("transactions/", TransactionAPIView.as_view(), name="transaction-list-create"),
    path("transactions/<int:pk>/", TransactionDetailAPIView.as_view(), name="transaction-detail"),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
    path("summary/<str:period>/", SummaryAPIView.as_view(), name="summary"),
]