from django.shortcuts import render, redirect
from .models import Vehiculo, Boleta, detalle_boleta
from .forms import VehiculoForm, RegistroUserForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from vehiculos.compra import Carrito


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def otra(request):
    autitos = Vehiculo.objects.raw('Select * from vehiculos_vehiculo')
    datos={
        'vehiculos':autitos
    }
    return render(request, 'otra.html', datos)

@login_required
def crear(request):
    if request.method=="POST":
        vehiculoform=VehiculoForm(request.POST,request.FILES)
        if vehiculoform.is_valid():
            vehiculoform.save()     #similar al insert en función
            return redirect ('otra')
    else:
        vehiculoform=VehiculoForm()
    return render (request, 'crear.html', {'vehiculoform': vehiculoform})

@login_required
def eliminar(request, id): 
    vehiculoEliminado = Vehiculo.objects.get(patente=id) #similar a select * from... where...
    vehiculoEliminado.delete()
    return redirect ('otra')

@login_required
def modificar(request, id): 
    vehiculoModificado=Vehiculo.objects.get(patente=id) #buscamos el objeto
    datos ={
        'form':VehiculoForm(instance=vehiculoModificado)
    }
    if request.method=="POST":
        formulario = VehiculoForm(data=request.POST, instance=vehiculoModificado)
        if formulario.is_valid():
            formulario.save()
            return redirect ('otra')
    return render(request, 'modificar.html', datos)


def registrar(request):
    data={                          #parámetro que llega al template
        'form': RegistroUserForm()
    }
    if request.method=="POST":
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()       #crear un objeto en el backend
            user = authenticate(username=formulario.cleaned_data["username"], 
                    password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect('index') 
        data["form"]=formulario           
    return render(request, 'registration/registrar.html',data)

def mostrar(request):
    autitos = Vehiculo.objects.all()
    datos={
        'autitos':autitos
    }
    return render(request, 'mostrar.html', datos)

 
def tienda(request):
    autitos = Vehiculo.objects.all()
    datos={
        'autitos':autitos
    }
    return render(request, 'tienda.html', datos)


def agregar_producto(request,id):
    carrito_compra= Carrito(request)
    vehiculo = Vehiculo.objects.get(patente=id)
    carrito_compra.agregar(vehiculo=vehiculo)
    return redirect('tienda')

def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    vehiculo = Vehiculo.objects.get(patente=id)
    carrito_compra.eliminar(vehiculo=vehiculo)
    return redirect('tienda')

def restar_producto(request, id):
    carrito_compra= Carrito(request)
    vehiculo = Vehiculo.objects.get(patente=id)
    carrito_compra.restar(vehiculo=vehiculo)
    return redirect('tienda')

def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')    


def generarBoleta(request):
    precio_total=0
    for key, value in request.session['carrito'].items():
        precio_total = precio_total + int(value['precio']) * int(value['cantidad'])
    boleta = Boleta(total = precio_total)
    boleta.save()
    productos = []
    for key, value in request.session['carrito'].items():
            producto = Vehiculo.objects.get(patente = value['vehiculo_id'])
            cant = value['cantidad']
            subtotal = cant * int(value['precio'])
            detalle = detalle_boleta(id_boleta = boleta, id_producto = producto, cantidad = cant, subtotal = subtotal)
            detalle.save()
            productos.append(detalle)
    datos={
        'productos':productos,
        'fecha':boleta.fechaCompra,
        'total': boleta.total
    }
    request.session['boleta'] = boleta.id_boleta
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'detallecarrito.html',datos)