from django.contrib import admin

# Register your models here.
from .models import Buscas,Configuracoes

admin.site.register(Buscas)
admin.site.register(Configuracoes)