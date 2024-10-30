from django.urls import path
from clientes import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('new/', views.create_cliente, name='create_cliente'),
    path('edit/<int:pk>/', views.update_cliente, name='update_cliente'),
    path('delete/<int:pk>/', views.delete_cliente, name='delete_cliente'),
    path('pdf/', views.generar_pdf_clientes, name='generar_pdf_clientes'),

    # rutas para login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # para que logout acepte peticiones get
    path('logout/', views.logout_view, name='logout'),

    #prueba registro de login
    path('register/', views.registro, name='registro'),

]
