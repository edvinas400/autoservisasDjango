from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


# Create your models here.

class AutomobilioModelis(models.Model):
    marke = models.CharField("Marke", max_length=200, help_text="Automobilio marke")
    modelis = models.CharField("Modelis", max_length=200, help_text="Automobilio modelis")

    def __str__(self):
        return f"{self.marke} {self.modelis}"

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField("Valstybinis numeris", max_length=200, help_text="Valstybinis numeris")
    automobilis = models.ForeignKey("AutomobilioModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField("VIN kodas", max_length=200, help_text="VIN kodas")
    klientas = models.CharField("Klientas", max_length=200, help_text="Klientas")
    cover = models.ImageField('Nuotrauka', upload_to='foto', null=True, blank=True)
    aprasymas = HTMLField(null = True, blank = True)
    def __str__(self):
        return f"{self.automobilis} {self.valstybinis_nr}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Uzsakymas(models.Model):
    data = models.DateTimeField("Data", null=True, blank=True)
    automobilis = models.ForeignKey("Automobilis", on_delete=models.CASCADE)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_data = models.DateField("Grazinimo data", null = True, blank=True)

    def is_overdue(self):
        return self.grazinimo_data and date.today() > self.grazinimo_data

    STATUSAS = (
        ('a', 'Atlikta'),
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('t', 'Atsaukta'),
    )
    statusas = models.CharField(max_length=1, choices=STATUSAS, default="p", blank=True, help_text="Statusas")

    def display_suma(self):
        sum = 0
        for eilute in self.eilutes.all():
            sum += eilute.display_kaina()
        return sum

    display_suma.short_description = 'Suma'

    def __str__(self):
        return f"{self.automobilis}"

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"


class Paslauga(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=200, help_text="Paslaugos pavadinimas")
    kaina = models.DecimalField("Kaina", decimal_places=2, max_digits=100)

    def __str__(self):
        return f"{self.pavadinimas}"

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey("Paslauga", on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey("Uzsakymas", on_delete=models.CASCADE, related_name="eilutes")
    kiekis = models.IntegerField("Kiekis", help_text="Kiekis")

    def display_kaina(self):
        return self.kiekis * self.paslauga.kaina

    display_kaina.short_description = 'Kaina'

    def __str__(self):
        return f"{self.uzsakymas} {self.paslauga}"

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"


class UzsakymoReview(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
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
        return f"{self.user.username} profilis"
    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"