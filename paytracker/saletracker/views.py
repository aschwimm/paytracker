from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from payplan.models import Sale, Payplan, VolumeBonus, Flat
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Avg
from django import forms
from django.shortcuts import redirect
from payplan.forms import DateForm
import datetime
from datetime import datetime

class LogSaleForm(forms.Form):
    profit = forms.IntegerField(label="Profit")

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    current_user = request.user
    if not Sale.objects.filter(salecredit=current_user).exists():
        return render(request, "saletracker/index.html", {
            "message": "No sales logged",
            "form": LogSaleForm(),
            "date": DateForm()

        })
    if request.method == "POST":
        form = DateForm(request.POST)
        current_user = request.user
        if form.is_valid():
            year = form.cleaned_data["year"]
            if not year:
                year = datetime.now().year
            month = form.cleaned_data["month"]
            print(month)
            sales = Sale.objects.filter(datelogged__month=month)
            if not Sale.objects.filter(datelogged__month=month, salecredit=current_user).exists():
                return render(request, "saletracker/index.html", {
            "message": "No sales logged",
            "form": LogSaleForm(),
            "date": DateForm(),
            })
            total_sales = sales.count()
            # Calculate appropriate volume bonus and commission rate
            payplan = Payplan.objects.all()
            bonus = VolumeBonus.objects.all()
            bonus = bonus.filter(sales_required__lte=total_sales).order_by('-bonus').first().bonus
            comm_rate = payplan.filter(totalsales__lte=total_sales).order_by('-commission').first().commission
            # Create variable for flat model querysets
            flat = Flat.objects.all()
            # Find appropriate flat amount, and seperate sales by sales whose profits * commission rate exceed the flat amount for sale
            flat = flat.filter(sales_required__lte=total_sales).order_by('-flat_amount').first().flat_amount
            payable_amount = 0
            flat_count = 0
            flat_sum = 0
            payable_profit = 0
            for sale in sales:
                if (sale.profit * (comm_rate / 100)) < flat:
                    payable_amount += flat
                    flat_count += 1
                    flat_sum += flat
                else:
                    payable_profit += sale.profit
            total_profit = payable_profit * 100
            # Calculate payable amount by current dollar amount in flats with total profit * commission percent, plus bonus for units sold
            payable_amount += ((total_profit * (comm_rate / 100)) / 100) + bonus
            # Calculate average earned per sale
            payable_average = sales.aggregate(Avg('profit'))
            payable_average = payable_average['profit__avg']
            total_profit = total_profit / 100
            comm_from_profit = payable_amount - flat_sum
            return render(request, "saletracker/index.html", {
                "sales": sales,
                "commission": format(comm_from_profit, ".2f"),
                "bonus": bonus,
                "total_sold": total_sales,
                "avg_earned": format(payable_average, ".2f"),
                "flat_count": flat_count,
                "flat_sum": flat_sum,
                "comm_rate": comm_rate,
                "earnings": format(payable_amount, ".2f"),
                "form": LogSaleForm(),
                "date": DateForm()
            })
    
    if  request.method == "GET":
        # Get current user object from logged in user and filter Sale model by sales credited to user's id
        
        current_user = request.user
        sales = Sale.objects.filter(salecredit=current_user.id)
        print(sales)
        if not sales:
            return render(request, "saletracker/index.html", {
            "message": "No sales logged",
            "form": LogSaleForm(),
            "date": DateForm(),
            })
        total_sales = sales.count()
        # Calculate appropriate volume bonus and commission rate
        payplan = Payplan.objects.all()
        bonus = VolumeBonus.objects.all()
        bonus = bonus.filter(sales_required__lte=total_sales).order_by('-bonus').first().bonus
        comm_rate = payplan.filter(totalsales__lte=total_sales).order_by('-commission').first().commission
        # Create variable for flat model querysets
        flat = Flat.objects.all()
        # Find appropriate flat amount, and seperate sales by sales whose profits * commission rate exceed the flat amount for sale
        flat = flat.filter(sales_required__lte=total_sales).order_by('-flat_amount').first().flat_amount
        payable_amount = 0
        flat_count = 0
        flat_sum = 0
        payable_profit = 0
        for sale in sales:
            if (sale.profit * (comm_rate / 100)) < flat:
                payable_amount += flat
                flat_count += 1
                flat_sum += flat
            else:
                payable_profit += sale.profit
        total_profit = payable_profit * 100
        # Calculate payable amount by current dollar amount in flats with total profit * commission percent, plus bonus for units sold
        payable_amount += ((total_profit * (comm_rate / 100)) / 100) + bonus
        # Calculate average earned per sale
        payable_average = sales.aggregate(Avg('profit'))
        payable_average = payable_average['profit__avg']
        total_profit = total_profit / 100
        return render(request, "saletracker/index.html", {
            "profit": format(total_profit, ".2f"),
            "sales": sales,
            "commission": format(payable_amount, ".2f"),
            "bonus": bonus,
            "total_sold": total_sales,
            "avg_earned": format(payable_average, ".2f"),
            "flat_count": flat_count,
            "flat_sum": flat_sum,
            "comm_rate": comm_rate,
            "earnings": format(payable_amount + bonus, ".2f"),
            "form": LogSaleForm(),
            "date": DateForm()
        })
def log(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "GET":
        return render(request, "saletracker/log.html", {
            "form": LogSaleForm()
        })
    if request.method == "POST":
        form = LogSaleForm(request.POST)
        if form.is_valid():
            profit = form.cleaned_data["profit"]
            username = request.user
            entry = Sale(profit=profit, salecredit=username)
            entry.save()
            return redirect("/saletracker")
def remove_log(request, pk):
    if request.method == "POST":
        current_user = request.user
        sales = Sale.objects.filter(salecredit=current_user.id, id=pk)
        sales.delete()
        return redirect("/saletracker/")
    return render(request, "saletracker/index.html")

    
    