# admin.py
from django.contrib import admin
from .models import UserStripe

# admin.py
import stripe
from django.conf import settings
from django.utils.html import format_html

@admin.register(UserStripe)
class UserStripeAdmin(admin.ModelAdmin):
    list_display = ['user', 'stripe_customer_id', 'stripe_bank_account_id', 'bank_account_details']
    
    def bank_account_details(self, obj):
        if obj.stripe_bank_account_id:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                bank_account = stripe.Customer.retrieve_source(
                    obj.stripe_customer_id,
                    obj.stripe_bank_account_id
                )
                return format_html(
                    "Bank: {}<br>Last 4: {}<br>Account Holder: {}",
                    bank_account.bank_name,
                    bank_account.last4,
                    bank_account.account_holder_name
                )
            except stripe.error.StripeError:
                return "Error retrieving bank account"
        return "No bank account"

    bank_account_details.short_description = "Bank Account Details"
