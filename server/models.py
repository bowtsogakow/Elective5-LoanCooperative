from .utils import generate_random_string
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from datetime import timedelta

class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, default=" ", null=True, blank=True, choices=[("admin", "admin"), ("client", "client"), ("cashier", "cashier")])
    full_name = models.CharField(max_length=255, null=True, blank=True)
    has_loan = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.first_name and self.middle_name and self.last_name:
            self.full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.full_name:
            return f"<{self.id}> {self.full_name}"
        else:
            return f"<{self.id}> {self.username}"


class ClientInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ClientInfos")
    address = models.TextField()
    contact_no = models.CharField(max_length=20)
    business = models.CharField(max_length=200, null=True, blank=True)  # Self-employed business name
    co_maker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="co_maker_clients")
    billing_statement_electric = models.ImageField(upload_to='billing_statements/', null=True, blank=True)
    billing_statement_water = models.ImageField(upload_to='billing_statements/', null=True, blank=True)

    def __str__(self):
        if self.user.full_name:
            return f"<{self.id}> {self.user.full_name}"
        return f"<{self.id}> {self.user.username}"
    
    def delete(self):
        self.billing_statement_electric.delete()
        self.billing_statement_water.delete()
        super().delete()
    

class Loan(models.Model):
    LOAN_TERMS = [(3, '3 months'), (6, '6 months'), (9, '9 months'), (12, '12 months')]
    INTEREST_MODE_CHOICES = [('Add-on', 'Add-on'), ('Less', 'Less')]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans") # input
    amount_loaned = models.DecimalField(max_digits=12, decimal_places=2) # input
    interest_percentage = models.DecimalField(max_digits=5, decimal_places=2) #input
    loan_term = models.IntegerField(choices=LOAN_TERMS) #input
    interest_mode = models.CharField(max_length=10, choices=INTEREST_MODE_CHOICES) # input
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2) #input 

    interest = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)   
    daily_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    days_total = models.IntegerField(null=True, blank=True)
    days_paid = models.IntegerField(null=True, blank=True)
    total_amount_paid = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    date_created = models.DateField(default=datetime.now().date())
    date_end = models.DateField(null=True, blank=True)
    date_paid = models.DateField(null=True, blank=True)
    status = models.CharField(default="ongoing", max_length=10, choices=[("ongoing", "ongoing"), ("completed", "completed")])
    qr_code = models.CharField(max_length=8, null=True, blank=True)  

    def compute_and_save(self, *args, **kwargs):
        random_code = generate_random_string()
        # Calculate interest and total before saving the loan
        temp = (self.amount_loaned * self.interest_percentage) / 100
        self.interest = temp * float(self.loan_term)
        self.processing_fee = self.amount_loaned * 0.02
        if self.interest_mode == "Add-on":
            self.total = self.amount_loaned + self.interest
        elif self.interest_mode == "Less":
            self.total = self.amount_loaned - self.interest
        else: 
            return None  # Invalid interest mode

        self.total = self.total + self.processing_fee
        self.days_total = float(self.loan_term) * 30
        self.days_paid = 0
        self.daily_payment = self.total / (float(self.loan_term) * 30)  # Assuming 30 days per month for simplicity
        self.qr_code = random_code
        self.status = "ongoing"
        self.total_payed = 0
        self.date_created = datetime.now().date()
        self.date_end = datetime.now().date() + timedelta(days=float(self.loan_term) * 30)
        
        self.client.has_loan = True
        self.client.save()

        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Loan for {self.client.full_name} ({self.amount_loaned})"
    

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2,)
    date = models.DateField(default=datetime.now().date())

    def update_loan_and_save(self, *args, **kwargs): 
        self.amount = self.loan.daily_payment
        self.loan.total_amount_paid += self.amount
        self.date = datetime.now().date()
        self.loan.days_paid += 1

        if self.loan.total_amount_paid >= self.loan.total:
            self.loan.status = "completed"
            self.loan.date_paid = datetime.now().date()
            self.loan.client.has_loan = False
           
        self.loan.save()

        super().save(*args, **kwargs)