from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    store_code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'store_code', 'password1', 'password2')
class LogSaleForm(forms.Form):
    profit = forms.IntegerField()
    
class RegisterPayplan(forms.Form):
    base_commission = forms.IntegerField()
    
class ScalingPayplan(forms.Form):
    commission_bump = forms.IntegerField()
    for_units_sold = forms.IntegerField()

class VolumeBonusForm(forms.Form):
    volume_bonus = forms.IntegerField(help_text="Enter total amount of volume bonus after hitting milestone")
    for_units_sold = forms.IntegerField(help_text="Sales required for bonus")

class FlatForm(forms.Form):
    flat_amount = forms.IntegerField()
    sales_required = forms.IntegerField(help_text="If flat amount does not scale with sales enter '0'")

class DateForm(forms.Form):
    choices = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December")
    ]
    year = forms.IntegerField(required=False)
    month = forms.ChoiceField(choices=choices)

'''class SaleSummaryForm(forms.Form):
    
    profit = forms.DecimalField()
    sales = forms.IntegerField()
    commission = forms.DecimalField()
    bonus = forms.IntegerField()
    total_sold = forms.IntegerField()
    avg_earned = forms.DecimalField()
    flat_total = forms.IntegerField()
    flat_sum = forms.IntegerField()
    comm_percent = forms.IntegerField()
    earnings = forms.DecimalField()'''

