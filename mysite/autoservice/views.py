from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.http import HttpResponse
from .forms import UzsakymoReviewForm, UserUpdateForm, ProfilisUpdateForm, UserUzsakymasCreateForm
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.

def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    uzsakymu_kiekis = Uzsakymas.objects.count()
    atlikti_uzsakymai = Uzsakymas.objects.filter(statusas__exact="a").count()
    automobiliu_kiekis = Automobilis.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    informacija = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'uzsakymu_kiekis': uzsakymu_kiekis,
        'atlikti_uzsakymai': atlikti_uzsakymai,
        'automobiliu_kiekis': automobiliu_kiekis,
        "vizitai": num_visits,
    }
    return render(request, 'index.html', context=informacija)


def automobiliai(request):
    paginator = Paginator(Automobilis.objects.all(), 1)
    page_number = request.GET.get("page")
    automobiliai = paginator.get_page(page_number)
    context = {
        "automobiliai": automobiliai
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


class UserUzsakymasCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ['data', 'automobilis']
    success_url = "/autoservice/manouzsakymai/"
    template_name = 'usernewuzsakymas.html'
    form_class = UserUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.instance.grazinimo_data = form.instance.data + datetime.timedelta(days=7)
        return super().form_valid(form)


class UserUzsakymoEiluteCreateView(LoginRequiredMixin, generic.CreateView):
    model = UzsakymoEilute
    fields = ['paslauga', 'kiekis']
    template_name = 'addeilute.html'

    def get_success_url(self):
        return reverse('uzsakymas', args=(self.object.uzsakymas.id,))

    def form_valid(self, form):
        form.instance.uzsakymas = Uzsakymas.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class UserUzsakymasUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    # fields = ['data', 'automobilis']
    success_url = "/autoservice/manouzsakymai/"
    template_name = 'usernewuzsakymas.html'
    form_class = UserUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.instance.grazinimo_data = form.instance.data + datetime.timedelta(days=7)
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class UserUzsakymasDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/autoservice/manouzsakymai/"
    template_name = 'deleteuzsakymas.html'

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class UserUzsakymaiListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    paginate_by = 2
    template_name = "useruzsakymai.html"
    context_object_name = "useruzsakymai"

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)


class UzsakymaiDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "uzsakymas"
    form_class = UzsakymoReviewForm

    def get_success_url(self):
        return reverse("uzsakymas", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(UzsakymaiDetailView, self).form_valid(form)


def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(
        Q(klientas__icontains=query) | Q(automobilis__marke__icontains=query) | Q(
            automobilis__modelis__icontains=query) | Q(vin_kodas__icontains=query) | Q(valstybinis_nr__icontains=query))
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profilis(request):
    return render(request, 'profilis.html')


@login_required
def editprofile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'editprofile.html', context)
