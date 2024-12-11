from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from .forms import UserRegisterForm, ExpenseForm
from .models import Expense, Balance


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            Balance.objects.create(user=user, initial_balance=0, current_balance=0)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    total_income = sum(t.amount for t in expenses if t.category == 'income')
    total_expense = sum(t.amount for t in expenses if t.category == 'expense')
    balance = total_income - total_expense  # Ensure balance is initialized

    return render(request, 'home.html', {
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    })

@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            # Update user balance
            balance = Balance.objects.get_or_create(user=request.user)[0]
            balance.update_balance(expense.amount)
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


from datetime import date
# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        picture = request.FILES.get('picture')
        if picture:
            profile = request.user.profile
            profile.picture = picture
            profile.save()
            return redirect('profile')  # Redirect back to the profile page
    return render(request, 'profile.html')

from datetime import date


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('index')  # Redirect to the home page or login page
    return render(request, 'profile.html')



from django.shortcuts import render, redirect
from .models import Budget
@login_required
def index(request):
    if request.method == "POST":
        description = request.POST.get('budget')
        if description:
            Budget.objects.create(description=description)
            return redirect('index')

    budgets = Budget.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'budgets': budgets})