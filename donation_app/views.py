from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from more_itertools import sliced
from datetime import date
from django.views import View
from django.shortcuts import render, redirect
from donation_app.models import Donation, Institution, Category
from donation_app.forms import CreateUserForm, UserUpdateForm, ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.


class LandingPageView(View):

    def get(self, request):
        form_contact = ContactForm()
        supported_institutions = []
        all_donations = Donation.objects.all()
        for query in all_donations:
            if query.institution not in supported_institutions:
                supported_institutions.append(query.institution)
        supported_institutions_count = len(supported_institutions)
        context = {'bags_counter': sum([x.quantity for x in Donation.objects.all()]),
                   'institutions_counter': supported_institutions_count,
                   'foundations': Institution.objects.filter(type='FOUNDATION').order_by('name'),
                   'ngos': Institution.objects.filter(type='NON-GOVERNMENTAL ORGANISATION').order_by('name'),
                   'local_charities': Institution.objects.filter(type='LOCAL CHARITY').order_by('name'),
                   'form_contact': form_contact
                   }
        return render(request, 'index.html', context)

    def post(self, request):
        if request.method == "POST":
            form_contact = ContactForm(request.POST)
            if form_contact.is_valid():
                subject = form_contact.cleaned_data["subject"]
                from_email = form_contact.cleaned_data["from_email"]
                message = form_contact.cleaned_data['message']
                try:
                    send_mail(subject, message, from_email, ["pu3ek.zip@vp.pl"])
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return render(request, 'email-confirmation.html')
        return redirect('index')


class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):
        context = {'categories': Category.objects.all().order_by('id'),
                   'institutions': Institution.objects.all()
        }
        return render(request, 'form.html', context)

    def post(self, request):
        quantity = int(request.POST['bags'])
        institution = request.POST['organization']
        phone_number = request.POST['phone']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        if len(request.POST['address']) < 129:
            address_1 = request.POST['address']
            address_2 = ''
        else:
            address_list = list(sliced(request.POST['adress'], 128))
            address_1 = address_list[0]
            address_2 = address_list[1]

        new_donation = Donation(quantity=quantity, institution_id=institution, phone_number=phone_number,
                                address_1=address_1, address_2=address_2, city=city, zip_code=zip_code,
                                pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                pick_up_comment=pick_up_comment, user=user)
        new_donation.save()
        for id in request.POST.getlist('categories'):
            new_donation.categories.add(id)
        return render(request, 'form-confirmation.html')


class UpdateDonationStatusView(View):

    def get(self, request, id):
        context = {'donation_to_be_updated': Donation.objects.get(id=id)}
        return render(request, 'form-status_update.html', context)

    def post(self, request, id):
        donation_to_be_updated = Donation.objects.get(id=id)
        choice_list = request.POST.getlist('status')
        if len(choice_list) == 1:
            donation_to_be_updated.is_taken = choice_list[0]
            if choice_list[0] == 'Zrealizowane':
                donation_to_be_updated.status_update_date = date.today()
            donation_to_be_updated.save()
            return redirect('user_profile')
        else:
            context = {
                'donation_to_be_updated': donation_to_be_updated,
                'errors': 'Jeżeli chcesz zmienić status zgłoszenia wybierz jedną z dostępnych opcji.'}
            return render(request, 'form-status_update.html', context)


class UserView(View):

    def get(self, request):
        context = {'user_donations': Donation.objects.filter(user_id=request.user.id).order_by('-pick_up_date').order_by('-status_update_date')}
        return render(request, 'user_profile.html', context)

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        elif user is None:
            return redirect('register')
        return render(request, 'login.html')


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/accounts/login/#login')
        return render(request, 'register.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'form-update_user.html', {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.save()
                messages.success(request, 'Twoje dane zostały zapisane')
                return redirect('user_profile')
        except IntegrityError as e:
            messages.error(request, 'Podany email jest już zarejestrowany!')
            return render(request, 'form-update_user.html', {'form': form})

class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'form-update_user.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione')
            return redirect('user_profile')
        else:
            messages.error(request, 'Błąd hasła')
            form = PasswordChangeForm(request.user)
            return render(request, 'form-update_user.html', {'form': form})

