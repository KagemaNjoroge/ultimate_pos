from django.db import models
from utils.models import TimestampedModel


class ExpenseCategory(TimestampedModel):
    category_name = models.CharField(
        max_length=100, blank=False, null=False, unique=True
    )
    category_description = models.CharField(max_length=300, blank=True, null=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        db_table = "ExpenseCategory"
        verbose_name_plural = "Expense Categories"
        verbose_name = "Expense Category"




class Expense(TimestampedModel):
    expense_name = models.CharField(
        max_length=100, blank=False, null=False, unique=True
    )
    expense_description = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)

    def __str__(self) -> str:
        return self.expense_name



    class Meta:
        db_table = "Expenses"
        verbose_name_plural = "Expenses"
        verbose_name = "Expense"
