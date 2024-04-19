from django.urls import path
from .views import AddGetProductsView, GetDeleteUpdateProductView



urlpatterns = [
    path('', AddGetProductsView.as_view(), name='get_user' ),
    path('', AddGetProductsView.as_view(), name='get_user' ),
    path('<int:pk>/', GetDeleteUpdateProductView.as_view(), name='get_user' ),
]

