from django.contrib import admin
from . import models


class UzsakymoEilutesInLine(admin.TabularInline):
    model = models.UzsakymoEilute
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ("automobilis", "data", "statusas", "vartotojas", "grazinimo_data", "display_suma")
    inlines = [UzsakymoEilutesInLine]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ("klientas", "automobilis", "valstybinis_nr", "vin_kodas")
    list_filter = ("klientas", "automobilis")
    search_fields = ("valstybinis_nr", "vin_kodas")


class UzsakymoEiluteAdmin(admin.ModelAdmin):
    list_display = ("paslauga", "kiekis", "uzsakymas", "display_kaina")


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "kaina")


# Register your models here.
admin.site.register(models.AutomobilioModelis)
admin.site.register(models.Automobilis, AutomobilisAdmin)
admin.site.register(models.Uzsakymas, UzsakymasAdmin)
admin.site.register(models.Paslauga, PaslaugaAdmin)
admin.site.register(models.UzsakymoEilute, UzsakymoEiluteAdmin)
