from .utils import generate_random_string
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, default=" ", null=True, blank=True, choices=[("admin", "admin"), ("client", "client"), ("cashier", "cashier")])
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



class ClientInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ClientInfos")
    address = models.TextField()
    contact_no = models.CharField(max_length=20)
    work_details = models.TextField(null=True, blank=True)
    business = models.CharField(max_length=200, null=True, blank=True)  # Self-employed business name
    co_maker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="co_maker_clients")
    billing_statement_electric = models.ImageField(upload_to='billing_statements/', null=True, blank=True)
    billing_statement_water = models.ImageField(upload_to='billing_statements/', null=True, blank=True)

    def __str__(self):
        return self.name
    
# models.py
class Loan(models.Model):
    LOAN_TERMS = [(3, '3 months'), (6, '6 months'), (9, '9 months'), (12, '12 months')]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans") # input
    amount_loaned = models.DecimalField(max_digits=12, decimal_places=2) # input
    interest_percentage = models.DecimalField(max_digits=5, decimal_places=2) #input
    loan_term = models.IntegerField(choices=LOAN_TERMS) #input
    interest_mode = models.CharField(max_length=10, choices=[('Add-on', 'Add-on'), ('Less', 'Less')]) # input
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)   
    days_total = models.IntegerField(null=True, blank=True)
    days_paid = models.IntegerField(null=True, blank=True)
    daily_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_payed = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    status = models.CharField(default="ongoing", max_length=10, choices=[("ongoing", "ongoing"), ("completed", "completed")])
    qr_code = models.CharField(max_length=8, null=True, blank=True)  

    def compute_and_save(self, *args, **kwargs):
        random_code = generate_random_string()
        # Calculate interest and total before saving the loan
        temp = (self.amount_loaned * self.interest_percentage) / 100
        self.interest = temp * self.loan_term
        self.processing_fee = self.amount_loaned * 0.02

        if self.interest_mode == "Add-on":
            self.total = self.amount_loaned + self.interest
        elif self.interest_mode == "Less":
            self.total = self.amount_loaned - self.interest
        else: 
            return None  # Invalid interest mode
        
        self.total = self.total + self.processing_fee
        self.days_total = self.loan_term * 30
        self.days_paid = 0
        self.daily_payment = self.total / (self.loan_term * 30)  # Assuming 30 days per month for simplicity
        self.qr_code = random_code
        self.status = "ongoing"
        self.total_payed = 0

        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Loan for {self.client.name} ({self.amount_loaned})"
    

