from django.contrib import admin

from server.models import ClientInfo, Loan, User, Payment

# Register your models here.

admin.site.register(User)
admin.site.register(Loan)
admin.site.register(ClientInfo)
admin.site.register(Payment)

