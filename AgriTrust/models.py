from django.db import models
from .utils import generate_random_string

# Create your models here.

# models.py
from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_no = models.CharField(max_length=20)
    work_details = models.TextField(null=True, blank=True)
    business = models.CharField(max_length=200, null=True, blank=True)  # Self-employed business name
    co_maker = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="co_maker_clients")
    billing_statement_electric = models.ImageField(upload_to='billing_statements/', null=True, blank=True)
    billing_statement_water = models.ImageField(upload_to='billing_statements/', null=True, blank=True)

    def __str__(self):
        return self.name
    
# models.py
class Loan(models.Model):
    LOAN_TERMS = [(3, '3 months'), (6, '6 months'), (9, '9 months'), (12, '12 months')]
    client = models.ForeignKey(Client, on_delete=models.CASCADE) # input
    amount_loaned = models.DecimalField(max_digits=12, decimal_places=2) # input
    interest_percentage = models.DecimalField(max_digits=5, decimal_places=2) #input
    loan_term = models.IntegerField(choices=LOAN_TERMS) #input
    interest = models.DecimalField(max_digits=12, decimal_places=2)
    interest_mode = models.CharField(max_length=10, choices=[('Add-on', 'Add-on'), ('Less', 'Less')])
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)  
    net_proceed = models.DecimalField(max_digits=12, decimal_places=2)  
    daily_payment = models.DecimalField(max_digits=10, decimal_places=2)
    total_payed = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    status = models.CharField(default="ongoing", max_length=10, choices=[("ongoing", "ongoing"), ("completed", "completed")])
    qr_code = models.CharField(max_length=8, null=True, blank=True)  

    def save(self, *args, **kwargs):
        random_code = generate_random_string()
        # Calculate interest and total before saving the loan
        self.interest = (self.amount_loaned * self.interest_percentage) / 100
        if self.interest_mode == "Add-on":
            self.total = self.amount_loaned + self.interest
        else:
            self.total = self.amount_loaned - self.interest
        self.net_proceed = self.total - self.processing_fee
        self.daily_payment = self.total / (self.loan_term * 30)  # Assuming 30 days per month for simplicity
        self.qr_code = random_code
        super(Loan, self).save(*args, **kwargs)

    def __str__(self):
        return f"Loan for {self.client.name} ({self.amount_loaned})"
    

