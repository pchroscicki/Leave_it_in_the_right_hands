from django.shortcuts import render

# Create your views here.
from django.views import View

from donation_app.models import Donation, Institution


class LandingPageView(View):

    def get(self, request):
        supported_institutions_count = self.supported_institutions_counter()
        context = {'bags_counter': sum([x.quantity for x in Donation.objects.all()]),
                   'institutions_counter': supported_institutions_count,
                   'foundations': Institution.objects.filter(type='FOUNDATION').order_by('name'),
                   'ngos': Institution.objects.filter(type='NON-GOVERNMENTAL ORGANISATION').order_by('name'),
                   'local_charities': Institution.objects.filter(type='LOCAL CHARITY').order_by('name')
                   }
        return render(request, 'index.html', context)

    @staticmethod
    def supported_institutions_counter():
        supported_institutions = []
        all_donations = Donation.objects.all()
        for query in all_donations:
            if query.institution not in supported_institutions:
                supported_institutions.append(query.institution)
        return len(supported_institutions)


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')

class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')