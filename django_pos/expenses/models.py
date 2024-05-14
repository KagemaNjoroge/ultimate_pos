from django.db import models


# Create your models here.
class ExpenseCategory(models.Model):
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

    def to_json(self) -> dict:
        return {
            "category_name": self.category_name,
            "category_description": self.category_description,
            "is_recurring": self.is_recurring,
            "id": self.id,
        }


class Expense(models.Model):
    expense_name = models.CharField(
        max_length=100, blank=False, null=False, unique=True
    )
    expense_description = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.expense_name

    def to_json(self) -> dict:
        return {
            "expense_name": self.expense_name,
            "expense_description": self.expense_description,
            "category": self.category.category_name,
            "amount": self.amount,
            "date_added": self.date_added,
            "date_modified": self.date_modified,
            "id": self.id,
        }

    class Meta:
        db_table = "Expenses"
        verbose_name_plural = "Expenses"
        verbose_name = "Expense"
