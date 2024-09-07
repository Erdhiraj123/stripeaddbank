# views.py
import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserStripe
from .forms import SignUpForm
from django.contrib.auth import login

stripe.api_key = settings.STRIPE_SECRET_KEY

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserStripe.objects.get_or_create(user=user)  # Ensure UserStripe object exists
            login(request, user)
            return redirect('bank_account_view')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def create_stripe_customer(user):
    customer = stripe.Customer.create(email=user.email)
    user_stripe, created = UserStripe.objects.get_or_create(user=user)
    user_stripe.stripe_customer_id = customer.id
    user_stripe.save()
    return customer.id


@login_required
def add_bank_account(request):
    
    if request.method == 'POST':
        user=request.user
        data = json.loads(request.body)
        bank_account_token = data.get('token')
        try:
            # Get or create Stripe customer for the user
            user_stripe = UserStripe.objects.filter(user=user).first()
            # breakpoint()
            if not user_stripe.stripe_customer_id:
                user_stripe.stripe_customer_id = create_stripe_customer(user_stripe)
                user_stripe.save()
            
            # Add the bank account to the Stripe customer
            bank_account = stripe.Customer.create_source(
                user_stripe.stripe_customer_id,
                source=bank_account_token
            )
            
            # Save the bank account ID in your database
            user_stripe.stripe_bank_account_id = bank_account.id
            user_stripe.save()

            return JsonResponse({'status': 'success', 'bank_account_id': bank_account.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def verify_bank_account(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        bank_account_id = data.get('bank_account_id')
        amounts = data.get('amounts')  # This should be a list of the amounts deposited

        try:
            # Verify the bank account
            stripe.Customer.verify_external_account(
                user_stripe.stripe_customer_id,
                external_account=bank_account_id,
                amounts=amounts
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def verify_bank_account_view(request):
    return render(request, 'verify_bank_account.html')

@login_required
def bank_account_view(request):
    return render(request, 'account.html', {'publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
