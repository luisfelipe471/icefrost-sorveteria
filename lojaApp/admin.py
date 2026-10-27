from django.contrib import admin
from .models import Categoria, Comentario, Fornecedor, OpcaoDietetica, Sorvete

admin.site.register(Categoria)
admin.site.register(Fornecedor)
admin.site.register(OpcaoDietetica)
admin.site.register(Sorvete)
admin.site.register(Comentario)