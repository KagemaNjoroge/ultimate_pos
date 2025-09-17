from rest_framework.viewsets import ModelViewSet
from .serializers import ExpenseCategorySerializer, ExpenseSerializer
from expenses.models import Expense, ExpenseCategory


class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
