from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#para busquedas
from django.db.models import Q  # Importa Q para realizar búsquedas complejas



#login_required para proteger ruta
@login_required
def create_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})

def cliente_list(request):
    # Sin búsquedas solo iría...
    #clientes = Cliente.objects.all()

    #con búsquedas
    query = request.GET.get("q")  # Obtén el término de búsqueda de los parámetros de URL
    if query:
        # Filtra los clientes con base en el nombre o apellidos
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(apellidos__icontains=query)
        )
    else:
        # Si no hay búsqueda, muestra todos los clientes
        clientes = Cliente.objects.all()

    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})

from django.shortcuts import get_object_or_404

@login_required
def update_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form , 'cliente': cliente})

@login_required
def delete_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})

# Reportes
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from .models import Cliente

def generar_pdf_clientes(request):

    # Crear el objeto HttpResponse con el encabezado PDF
    response = HttpResponse(content_type='application/pdf')
    # attachment lo descarga, inline lo abre
    response['Content-Disposition'] = 'inline; filename="clientes.pdf"'

    # Crear el objeto Canvas para el PDF
    #pdf = canvas.Canvas(response, pagesize=letter)
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Configuración inicial
    pdf.setTitle("Reporte de Clientes")

    # Título del PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 40, "Lista de Clientes")

    # Variables para el pie de página
    fecha_generacion = datetime.date.today().strftime("%Y-%m-%d")
    pagina_num = 1

    # Función para agregar pie de página
    def agregar_pie_de_pagina(pdf, pagina_num):
        pdf.setFont("Helvetica", 10)
        # Escribir la fecha en la esquina inferior izquierda
        pdf.drawString(30, 20, f"Fecha de generación: {fecha_generacion}")
        # Escribir el número de página en el pie
        pdf.drawString(width - 100, 20, f"Página núm. {pagina_num}")

    # Encabezados de tabla
    pdf.setFont("Helvetica-Bold", 12)
    encabezados = ["Nombre", "Apellidos", "Fecha de nac.", "Pais"]
    x_inicial = 100
    y = height - 80

    for i, encabezado in enumerate(encabezados):
        pdf.drawString(x_inicial + i * 150, y, encabezado)

    # Línea divisoria debajo de los encabezados
    y -= 10
    pdf.line(100, y, width - 100, y)

    # Espacio para los datos de clientes
    y -= 20

    # Obtener la lista total de clientes
    #clientes = Cliente.objects.all()

    # Filtrar 
    query = request.GET.get("q")
    if query:
        # Filtra los clientes por nombre o apellido
        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(apellidos__icontains=query)
        )
    else:
        # Muestra todos los clientes si no hay búsqueda
        clientes = Cliente.objects.all()


    # Posición inicial para los datos de clientes
    # y = height - 80

    # Añadir los datos de los clientes al PDF
    pdf.setFont("Helvetica", 12)
    for cliente in clientes:
        #pdf.drawString(100, y, f"Nombre: {cliente.nombre} {cliente.apellidos}")
        #pdf.drawString(100, y - 15, f"Fecha de Ingreso: {cliente.fecha_nac}")
        #pdf.drawString(100, y - 30, f"Email: {cliente.pais}")
        #y -= 60  # Decrementa el valor de Y para la siguiente fila

        #if y <= 40:
        #    pdf.showPage()  # Crear una nueva página si no hay espacio
        #    y = height - 40

        pdf.drawString(100, y, cliente.nombre)
        pdf.drawString(250, y, cliente.apellidos)
        pdf.drawString(400, y, cliente.fecha_nac.strftime("%Y-%m-%d"))
        pdf.drawString(550, y, cliente.pais)
        
        y -= 20

        # Comprobar si es necesario cambiar de página
        if y <= 50:
            agregar_pie_de_pagina(pdf, pagina_num)
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = height - 80

            # Volver a dibujar los encabezados en la nueva página
            for i, encabezado in enumerate(encabezados):
                pdf.drawString(x_inicial + i * 150, y, encabezado)
            y -= 10
            pdf.line(100, y, width - 100, y)
            y -= 20

            # Incrementar el número de página
            pagina_num += 1

    # Agregar pie de página a la última página
    agregar_pie_de_pagina(pdf, pagina_num)

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    return response


from django.shortcuts import render, redirect
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión o a donde prefieras