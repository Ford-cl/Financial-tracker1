from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    # @staticmethod
    # def get_total_expenditure(user):
    #     """Calculate the total expenditure for a user."""
    #     total_expense = Expense.objects.filter(user=user).aggregate(models.Sum('amount'))['amount__sum'] or 0
    #     return total_expense

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Balance: {self.current_balance}"

    def update_balance(self, amount):
        """Subtract the expense from the current balance."""
        self.current_balance -= amount
        self.save()


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def _str_(self):
        return f"{self.user.username}'s Profile"

from django.db import models

class Budget(models.Model):
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"