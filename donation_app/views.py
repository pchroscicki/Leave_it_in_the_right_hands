from django.shortcuts import render

# Create your views here.
from django.views import View

from donation_app.models import Donation


class LandingPageView(View):

    def get(self, request):
        all_bags = self.donated_bags_counter()
        supported_institutions = self.supported_institutions_counter()
        context = {'bags_counter': all_bags, 'institutions_counter': supported_institutions}
        return render(request, 'index.html', context)

    @staticmethod
    def donated_bags_counter():
        bags_list = [x.quantity for x in Donation.objects.all()]
        return sum(bags_list)

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