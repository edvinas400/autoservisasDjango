from django.db import models


# Create your models here.

class AutomobilioModelis(models.Model):
    marke = models.CharField("Marke", max_length=200, help_text="Automobilio marke")
    modelis = models.CharField("Modelis", max_length=200, help_text="Automobilio modelis")

    def __str__(self):
        return f"{self.marke} {self.modelis}"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField("Valstybinis numeris", max_length=200, help_text="Valstybinis numeris")
    modelis = models.ForeignKey("AutomobilioModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField("VIN kodas", max_length=200, help_text="VIN kodas")
    klientas = models.CharField("Klientas", max_length=200, help_text="Klientas")

    def __str__(self):
        return f"{self.modelis} {self.modelis}"


class Uzsakymas(models.Model):
    data = models.DateField("Data")
    automobilis = models.ForeignKey("Automobilis", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.automobilis} {self.data}"


class Paslauga(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=200, help_text="Paslaugos pavadinimas")
    kaina = models.FloatField("Kaina")

    def __str__(self):
        return f"{self.pavadinimas}"


class UzsakymoEilute(models.Model):
    paslauga = models.ForeignKey("Paslauga", on_delete=models.CASCADE)
    uzsakymas = models.ForeignKey("Uzsakymas", on_delete=models.CASCADE)
    kiekis = models.IntegerField("Kiekis", help_text="Kiekis")

    def __str__(self):
        return f"{self.uzsakymas} {self.paslauga}"
