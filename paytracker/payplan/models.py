from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
# Create your models here.
# Join models on unit count after a users model has been created

class Sale(models.Model):
    profit = models.IntegerField()
    salecredit = models.ForeignKey(User, on_delete=models.CASCADE)
    datelogged = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Profit: ${self.profit} Credit:{self.salecredit} Date:{self.datelogged}"
    
class Payplan(models.Model):
    commission = models.IntegerField(default=0)
    totalsales = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.totalsales != 0:
            return f"{self.commission}% commission per sale after {self.totalsales} sales."
        else:
            return f"{self.commission}% base commission"

class VolumeBonus(models.Model):
    bonus = models.IntegerField(default=0)
    sales_required = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "volume bonuses"
    
    def __str__(self):
        return  f"${self.bonus} bonus for {self.sales_required} sales."

class Flat(models.Model):
    flat_amount = models.IntegerField(default=0)
    sales_required = models.IntegerField(default=0, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        if self.sales_required != 0:
            return  f"${self.flat_amount} flat after {self.sales_required} sales."
        else:
            return f"${self.flat_amount} flats"
class UserModel(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    store_code = models.CharField(max_length=50)
    def __str__(self):
        return  f"First name: {self.first_name} Last name: {self.last_name} Username: {self.username} Email: {self.email} Store code: {self.store_code}"
#Need a foreign key to join sales table with users table to determine which person gets credit for a sale
#Write a loop in a view to calculate commission if user sales are greater than totalsales in Payplan model