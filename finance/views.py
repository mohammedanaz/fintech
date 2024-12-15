from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Income
from .serializers import IncomeListSerializer, IncomeCreateSerializer

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
        return {'request': self.request}
    
class IncomeDeleteView(generics.DestroyAPIView):
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated]