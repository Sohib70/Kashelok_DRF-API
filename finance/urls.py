from django.urls import path
from .views import CategoryListCreateView, TransactionListCreateView, DashboardAPIView, SummaryAPIView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('transactions/', TransactionListCreateView.as_view()),
    path('dashboard/', DashboardAPIView.as_view()),
    path('summary/<str:period>/', SummaryAPIView.as_view()),
]
