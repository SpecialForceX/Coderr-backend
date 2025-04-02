from django.urls import path
from .views import (
    OrderListCreateView, OrderUpdateView, OrderDeleteView,
    InProgressOrderCountView, CompletedOrderCountView
)

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders'),
    path('<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('order-count/<int:business_user_id>/', InProgressOrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]
