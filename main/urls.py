from django.urls import path
from . import views
from .views import chatbot_response

urlpatterns = [
    path('', views.home, name='home'),
    path('screen2/', views.pantalla2, name='pantalla2'),
    path('atencion/', views.atencion_cliente, name='atencion1'),
    path('atencion2/', views.atenciondos, name='atencion2'),
    path('chat_ia/', views.chat_ia, name='chat_ia'),
    path('reclamo/', views.reclamo, name='reclamo1'),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),
]
