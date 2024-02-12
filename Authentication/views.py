
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from Authentication.models import Utilisateur
from django.contrib import messages
import stripe
from django.urls import reverse
from Flow.views import *


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Utilisateur.objects.create(user=user, name=form.cleaned_data.get(
                'pseudo'), email=user.username)  # Crée le profil client associé
            login(request, user)
            # Rediriger vers la page d'accueil après l'inscription
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Authentication/signin.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'Authentication/login.html'
    def get_success_url(self):
        return reverse('profile')  # Obtient l'URL à partir du nom de la route

def show_profile(request):
    if request.user.is_authenticated:
        user = Utilisateur.objects.get(user=request.user)
        return render(request, 'Authentication/show_profile.html', {'user': user})
    else:
        return render(request, 'Authentication/signin.html')


def modify_profile(request):
    if request.user.is_authenticated:
        user = Utilisateur.objects.get(user=request.user)
        if request.method == 'POST':
            form = UtilisateurForm(request.POST, request.FILES, instance=user)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = UtilisateurForm(instance=user)
        return render(request, 'Authentication/modify_profile.html', {'form': form})
    else:
        return redirect('login')


def request_vendor_status(request):
    if request.method == 'POST':
        utilisateur = Utilisateur.objects.get(user=request.user)
        utilisateur.money_man_request_pending = True
        utilisateur.save()
        return redirect('profile')
    return redirect('home')


# clé secrète Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_connect_account(request):
    if not request.user.is_authenticated:
        messages.error(
            request, "Vous n'êtes pas autorisé à effectuer cette action.")
        return redirect('profile')
    user = Utilisateur.objects.get(user=request.user)
    if not user.is_validated_money_man:
        messages.error(
            request, "Vous n'êtes pas autorisé à effectuer cette action.")
        return redirect('profile')
    try:
        # Création du compte Stripe Connect pour l'utilisateur
        account = stripe.Account.create(
            type="express",
            country="FR",
            email=user.email,
            capabilities={"card_payments": {"requested": True},
                          "transfers": {"requested": True}},
            business_type="individual",
        )

        # Enregistrer l'ID du compte Connect avec l'utilisateur
        user.stripe_account_id = account.id
        user.save()

        # Redirection vers l'interface de configuration du compte Stripe
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url=request.build_absolute_uri('/profile/'),
            return_url=request.build_absolute_uri('/profile/'),
            type="account_onboarding",
        )

        return redirect(account_link.url)
    except stripe.error.StripeError as e:
        messages.error(
            request, "Une erreur est survenue lors de la création du compte Stripe.")
        return redirect('profile')
    
def checkout(request, event_id):
    event = Event.objects.get(id=event_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Ticket pour l\'event : ' + event.title,
                },
                'unit_amount': int(event.ticket_price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('JoinEventConfirm', args=(event_id,))),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    if request.user.is_authenticated:
        client = Utilisateur.objects.get(user=request.user)
        cart = TinyCart.objects.get(client=client)

        # Créer une nouvelle commande
        reservation = Reservation.objects.create(
            client=client,
            total_price=cart.total_price,
            is_paid=True
        )

        return render(request, 'Authentication/payment_success.html')
    else:
        return redirect('login')


def payment_cancel(request):
    return render(request, 'Authentication/payment_cancel.html')
