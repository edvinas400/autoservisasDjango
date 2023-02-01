from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


# Create your models here.

class AutomobilioModelis(models.Model):
    marke = models.CharField(_("Make"), max_length=200, help_text="Automobilio marke")
    modelis = models.CharField(_("Model"), max_length=200, help_text="Automobilio modelis")

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = _("Car model")
        verbose_name_plural = _("Car models")


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(_("License plate"), max_length=200, help_text="Valstybinis numeris")
    automobilis = models.ForeignKey("AutomobilioModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(_("VIN code"), max_length=200, help_text="VIN kodas")
    klientas = models.CharField(_("Customer"), max_length=200, help_text="Klientas")
    cover = models.ImageField(_('Picture'), upload_to='foto', null=True, blank=True)
    aprasymas = HTMLField(null = True, blank = True)
    def __str__(self):
        return f"{self.automobilis} {self.valstybinis_nr}"

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")


class Uzsakymas(models.Model):
    data = models.DateTimeField(_("Date"), null=True, blank=True)
    automobilis = models.ForeignKey("Automobilis", on_delete=models.CASCADE)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_data = models.DateField(_("Return date"), null = True, blank=True)

    def is_overdue(self):
        return self.grazinimo_data and date.today() > self.grazinimo_data

    STATUSAS = (
        ('a', _('Done')),
        ('p', _('Accepted')),
        ('v', _('In progress')),
        ('t', _('Canceled')),
    )
    statusas = models.CharField(max_length=1, choices=STATUSAS, default="p", blank=True, help_text="Statusas")

    def display_suma(self):
        sum = 0
        for eilute in self.eilutes.all():
            sum += eilute.display_kaina()
        return sum

    display_suma.short_description = _('Total')

    def __str__(self):
        return f"{self.automobilis}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class Paslauga(models.Model):
    pavadinimas = models.CharField(_("Name"), max_length=200, help_text="Paslaugos pavadinimas")
    kaina = models.DecimalField(_("Price"), decimal_places=2, max_digits=100)

    def __str__(self):
        return f"{self.pavadinimas}"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey("Paslauga", on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey("Uzsakymas", on_delete=models.CASCADE, related_name="eilutes")
    kiekis = models.IntegerField(_("Amount"), help_text="Kiekis")

    def display_kaina(self):
        return self.kiekis * self.paslauga.kaina

    display_kaina.short_description = _('Price')

    def __str__(self):
        return f"{self.uzsakymas} {self.paslauga}"

    class Meta:
        verbose_name = _("Order line")
        verbose_name_plural = _("Order lines")


class UzsakymoReview(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(_('Review'), max_length=2000)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _('Reviews')
        ordering = ['-date_created']

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profilis")
    foto = models.ImageField(default="default.png", upload_to="profile_pics", null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.foto.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.foto.path)

    def __str__(self):
        return _("%s profile") %self.user.username
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")