from rest_framework import viewsets

from ..ser.expenses import ExpenseSerializer, ExpenseCategorySerializer, Expense, ExpenseCategory


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
