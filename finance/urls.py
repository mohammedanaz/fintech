from django.urls import path
from .views import *

urlpatterns = [
    path('income-list/', IncomeListView.as_view(), name='income-list'),
    path('income-create/', IncomeCreateView.as_view(), name='income-create'),
    path('income-delete/<int:pk>', IncomeDeleteView.as_view(), name='income-delete'),
]