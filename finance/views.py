from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from .models import Income
from .serializers import *
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status


class IncomeListView(generics.ListAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the returned income to the authenticated user.
        """
        return self.queryset.filter(user=self.request.user)


class IncomeCreateView(generics.CreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Pass the request to the serializer for access to `request.user`
        return {"request": self.request}


class IncomeDeleteView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated]


class IncomeUpdateView(generics.UpdateAPIView):
    serializer_class = IncomeUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        income_id = self.request.data.get("id")
        if not income_id:
            raise ValidationError({"id": "This field is required."})

        try:
            return Income.objects.get(id=income_id, user=self.request.user)
        except Income.DoesNotExist:
            raise NotFound("Income record not found or not authorized to access it.")


class IncomeChartData(APIView):
    """To manage api for Income chart display"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_income = Income.objects.filter(user=request.user)
        data = (
            user_income.annotate(month=TruncMonth("date_received"))
            .values("month")
            .annotate(monthly_income=Sum("amount"))
            .order_by("month")
        )
        response_data = [
            ( item["month"].strftime("%b"), float(item["monthly_income"]))
            for item in data
        ]
        return Response({'data': response_data}, status=status.HTTP_200_OK)