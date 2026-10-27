from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cardapio/', views.mostrar_cardapio, name='cardapio'),
    path('galeria/', views.galeria, name='galeria'),
    path('feedback/', views.feedback, name='feedback'),
    path('cadastrar_sorvete/', views.cadastrar_sorvete, name='cadastrar_sorvete'),
    path('editar/<int:sorvete_id>/', views.editar_sorvete, name='editar_sorvete'),
    path('excluir/<int:sorvete_id>/', views.excluir_sorvete, name='excluir_sorvete'),
    path('comentario/<int:sorvete_id>/', views.comentario_sorvete, name='comentario_sorvete'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('logout/', views.logout_view, name='logout'),
]
