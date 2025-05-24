from django.shortcuts import render
from . models import Payplan, Flat, VolumeBonus
from django.http import HttpResponseRedirect
from django.urls import reverse
from payplan.forms import RegisterPayplan, ScalingPayplan, FlatForm, VolumeBonusForm
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    current_user = request.user
    payplan = Payplan.objects.filter(user_id=current_user)
    flat = Flat.objects.filter(user_id=current_user)
    volume_bonus = VolumeBonus.objects.filter(user_id=current_user)
    if not payplan:
        if not flat:
            if not volume_bonus:
                return render(request, "payplan/payplan-select.html", {
                    "message": "No payplan saved"
                })
    return render(request, "payplan/index.html", {
        "payplan": payplan,
        "flat": flat,
        "volume_bonus": volume_bonus,
    })

def select_payplan(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "payplan/payplan-select.html")

def add_payplan(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.method == "GET":
        current_user = request.user
        payplan = Payplan.objects.filter(user_id=current_user)
        print(payplan)
        if payplan:
            return render(request, "payplan/scale-payplan.html", {
                "payplan": payplan,
                "form": ScalingPayplan()
            })
        return render(request, "payplan/add-payplan.html", {
            "comm_form": RegisterPayplan()
        })
    if request.method == "POST":
        form = RegisterPayplan(request.POST)
        if form.is_valid():
            commission = form.cleaned_data["base_commission"]
            current_user = request.user
            entry_commission = Payplan(commission=commission, user_id=current_user)
            entry_commission.save()
            return HttpResponseRedirect(reverse("payplan:index"))
def add_level(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    current_user = request.user
    if request.method == "POST":
        form = ScalingPayplan(request.POST)
        if form.is_valid():
            commission = form.cleaned_data["commission_bump"]
            units = form.cleaned_data["for_units_sold"]
            entry = Payplan(commission=commission, totalsales=units, user_id=current_user)
            entry.save()
            return HttpResponseRedirect(reverse("payplan:index"))
    return render(request, "payplan/edit.html", {
        "payplan": Payplan.objects.filter(user_id=current_user),
        "message": "No payplans saved"
    })
    
def update_payplan(request, pk):
    if request.method == "GET":
        current_user = request.user
        return render(request, "payplan/update-entry.html", {
            "payplan": Payplan.objects.filter(user_id=current_user, id=pk),
            "form": ScalingPayplan(),
            "message": "No payplans saved"
        })
    if request.method == "POST":
        if 'remove' in request.POST:
            current_user = request.user
            Payplan.objects.filter(id=pk).delete()
            return HttpResponseRedirect(reverse("payplan:edit"))
        elif 'update' in request.POST:
            form = ScalingPayplan(request.POST)
            if form.is_valid():
                commission = form.cleaned_data["commission_bump"]
                units = form.cleaned_data["for_units_sold"]
                Payplan.objects.filter(id=pk).update(commission=commission, totalsales=units)
                return HttpResponseRedirect(reverse("payplan:edit"))
def add_flat(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.method == "GET":
        return render(request, "payplan/add-flat.html", {
            "form": FlatForm()
        })
    if request.method == "POST":
        form = FlatForm(request.POST)
        if form.is_valid():
            current_user = request.user
            flat = form.cleaned_data["flat_amount"]
            sales_required = form.cleaned_data["sales_required"]
            entry = Flat(flat_amount=flat, sales_required=sales_required, user_id=current_user)
            entry.save()
            return HttpResponseRedirect(reverse("payplan:index"))
def add_volume_bonus(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    if request.method == "GET":
        return render(request, "payplan/add-volume-bonus.html", {
            "form": VolumeBonusForm()
        })
    if request.method == "POST":
        form = VolumeBonusForm(request.POST)
        if form.is_valid():
            current_user = request.user
            volume_bonus = form.cleaned_data["volume_bonus"]
            sales_required = form.cleaned_data["for_units_sold"]
            entry = VolumeBonus(bonus=volume_bonus, sales_required=sales_required, user_id=current_user)
            entry.save()
            return HttpResponseRedirect(reverse("payplan:index"))