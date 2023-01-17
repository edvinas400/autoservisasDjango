from django.db import models


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

    def __str__(self):
        return f"{self.automobilis} {self.valstybinis_nr}"

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Uzsakymas(models.Model):
    data = models.DateTimeField("Data")
    automobilis = models.ForeignKey("Automobilis", on_delete=models.CASCADE)

    def display_suma(self):
        sum = 0
        for eilute in self.eilutes.all():
            sum+=eilute.display_kaina()
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
