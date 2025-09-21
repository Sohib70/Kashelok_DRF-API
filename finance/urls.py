from django.urls import path
from .views import (CategoryListCreateView,TransactionListCreateView, TransactionDetailView,
    DashboardAPIView, SummaryAPIView,)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),

    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list-create"),
    path("transactions/<int:pk>/", TransactionDetailView.as_view(), name="transaction-detail-api"),

    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
    path("summary/<str:period>/", SummaryAPIView.as_view(), name="summary"),
]