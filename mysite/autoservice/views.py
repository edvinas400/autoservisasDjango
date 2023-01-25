from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    uzsakymu_kiekis = Uzsakymas.objects.count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(statusas__exact = "a").count()
    automobiliu_kiekis = Automobilis.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    informacija = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'uzsakymu_kiekis': uzsakymu_kiekis,
        'atlikti_uzsakymai': atlikti_uzsakymai,
        'automobiliu_kiekis': automobiliu_kiekis,
        "vizitai" : num_visits,
    }
    return render(request, 'index.html', context=informacija)
def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 1)
    page_number = request.GET.get("page")
    automobiliai = paginator.get_page(page_number)
    context = {
        "automobiliai" : automobiliai
    }
    return render(request, "automobiliai.html", context=context)
def automobilis(request, automobilis_id):
    automobilis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, "automobilis.html", {"automobilis": automobilis})
class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 1
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"

class UserUzsakymaiListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 2
    template_name = "useruzsakymai.html"
    context_object_name = "useruzsakymai"
    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)
class UzsakymaiDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"

def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(klientas__icontains=query) | Q(automobilis__marke__icontains=query) | Q(automobilis__modelis__icontains=query) | Q(vin_kodas__icontains=query) | Q(valstybinis_nr__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})