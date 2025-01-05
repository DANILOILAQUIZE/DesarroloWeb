from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from.models import PerfilUsuario, Categoria, Libro, Transacciones
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'index.html')

def perfil_usuario(request):
    usuario = request.user  # Obtener el usuario logueado
    return render(request, 'perfil_usuario.html', {'usuario': usuario})

def listar_libros(request):
    libros = Libro.objects.all()
    return render(request, 'detalle/librosVenta.html', {'libros': libros})

def detalles_libro(request, id):
    libro=Libro.objects.get(id=id)
    return render(request, 'detalle/detalleLibro.html', {'libro': libro})
#=======================================================================================================
#INICIAR SESION
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:  # Comparar con la contraseña sin encriptar
                login(request, user)
                return redirect('listar_usuarios')  # Redirigir a la lista de usuarios después de iniciar sesión
            else:
                # Si la contraseña no coincide
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos.'})

        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario no encontrado.'})

    return render(request, 'login.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('login')

#=======================================================================================================
#REGISTRAR USUARIO
def registrar_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Contraseña en texto plano
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        rol = request.POST.get('rol', 'Comprador')  # Valor por defecto

        # Crear el usuario sin encriptar la contraseña
        user = User(username=username, email=email, password=password)  # Aquí no usamos create_user
        user.save()

        # Crear el perfil de usuario
        PerfilUsuario.objects.create(
            user=user,
            telefono=telefono,
            direccion=direccion,
            rol=rol
        )
        # Mensaje de éxito
        messages.success(request, "¡Usuario registrado exitosamente!")
        return redirect('login')  # Redirigir a la página de inicio de sesión

    return render(request, 'Usuario/registrar_usuario.html')
#LISTAR USUARIOS

def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'Usuario/listar_usuarios.html', {'usuarios': usuarios})
#EDITAR USUARIO
# Vista para mostrar el formulario de edición del usuario
def editarUsuario(request, id):
    usuario = User.objects.get(id=id)
    return render(request, "Usuario/actualizar_usuarios.html", {'usuario': usuario})
#ACTUALIZAR USUARIO
# Vista para procesar la edición del usuario
def procesarEdisionUsuario(request):
    usuario = User.objects.get(id=request.POST["id"])
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    telefono = request.POST['telefono']
    direccion = request.POST['direccion']
    
    usuario.username = username
    usuario.email = email
    usuario.password = password
    usuario.save()
    
    # Si el usuario tiene un perfil, actualizamos sus datos adicionales
    if hasattr(usuario, 'perfil'):
        usuario.perfil.telefono = telefono
        usuario.perfil.direccion = direccion
        usuario.perfil.save()
    # Mensaje de éxito
    messages.success(request, "¡Usuario actualizado exitosamente!")
    return redirect('listar_usuarios')
#ELIMINAR USUARIO
def eliminar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    # Mensaje de éxito
    messages.success(request, "¡Usuario eliminado exitosamente!")
    return redirect('listar_usuarios')


#=============================================================================================
#CRUD CATEGORIA
def listarCategoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'Categoria/listarCategoria.html', {'categorias': categorias})

def agregarCategoria(request):
    return render(request, 'Categoria/agregarCategoria.html')

def guardarCategoria(request):
    nombre = request.POST.get('nombre')
    Categoria.objects.create(nombre=nombre)
    # Mensaje de éxito
    messages.success(request, "¡Categoria ingresado exitosamente!")
    return redirect('listarCategoria')


def eliminarCategoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    messages.success(request, "¡Categoria eliminado exitosamente!")
    return redirect('listarCategoria')

#=============================================================================================
#CRUD LIBRO
def agregarLibro(request):
    categorias = Categoria.objects.all()
    libros = Libro.objects.all()
    return render(request, 'libros/agregarLibro.html', {'categorias': categorias, 'libros': libros})

def agregarLibro(request):
    categorias = Categoria.objects.all()
    usuarios_vendedores = User.objects.filter(perfil__rol='Vendedor')  # Solo vendedores
    return render(request, 'libros/agregarLibro.html', {
        'categorias': categorias,
        'usuarios_vendedores': usuarios_vendedores
    })

def guardarLibro(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        precio = request.POST['precio']
        disponible = request.POST.get('disponible') == 'on'  # Checkbox para disponibilidad
        categoria_id = request.POST['categoria']
        vendedor_id = request.POST['vendedor']
        imagen = request.FILES.get('imagen')  # Archivo de imagen
        
        # Validación y búsqueda de categoría y vendedor
        categoria = Categoria.objects.get(id=categoria_id)
        vendedor = User.objects.get(id=vendedor_id)
        
        # Crear el libro
        Libro.objects.create(
            titulo=titulo,
            autor=autor,
            precio=precio,
            categoria=categoria,
            vendedor=vendedor,
            imagen=imagen,
            disponible=disponible
        )
        messages.success(request, "¡Libro ingresado exitosamente!")
        return redirect('listarLibro')  # Redirigir al listado de libros
    else:
        return redirect('listarLibro')  # Si no es POST, redirigir al formulario


def listarLibro(request):
    libros = Libro.objects.all()
    return render(request, 'libros/listarLibro.html', {'libros': libros})


def editarLibro(request, id):
    libro = Libro.objects.get(id=id)
    categorias = Categoria.objects.all()
    vendedores = User.objects.filter(perfil__rol='Vendedor')  # Filtra solo los vendedores

    return render(request, 'libros/editarLibro.html', {
        'libro': libro,
        'categorias': categorias,
        'vendedores': vendedores
    })

def actualizarLibro(request, id):
    if request.method == 'POST':
        libro = Libro.objects.get(id=id)
        libro.titulo = request.POST['titulo']
        libro.autor = request.POST['autor']
        libro.precio = request.POST['precio']
        libro.categoria = Categoria.objects.get(id=request.POST['categoria'])
        libro.vendedor = User.objects.get(id=request.POST['vendedor'])
        libro.disponible = request.POST['disponible'] == 'True'

        if 'imagen' in request.FILES:
            libro.imagen = request.FILES['imagen']

        libro.save()
        messages.success(request, "¡Libro editado exitosamente!")
        return redirect('listarLibro')

def eliminarLibro(request, id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    messages.success(request, "¡Libro eliminado exitosamente!")
    return redirect('listarLibro')

 #=============================================================================================
 #CRUD TRANSACCIONES
 


def agregarTransaccion(request):
    libros = Libro.objects.filter(disponible=True).order_by('-id')  # Solo libros disponibles y ordenados por el más reciente
    usuarios_compradores = User.objects.filter(perfil__rol='Comprador')  # Solo compradores

    return render(request, 'transacciones/agregarTransacciones.html', {
        'libros': libros,
        'usuarios_compradores': usuarios_compradores,
    })

def guardarTransaccion(request):
    if request.method == 'POST':
        comprador_id = request.POST.get('comprador')
        libro_id = request.POST.get('libro')
        estado = request.POST.get('estado')

        comprador = User.objects.get(id=comprador_id)
        libro = Libro.objects.get(id=libro_id)

        # Obtener el precio directamente desde el libro seleccionado
        precio = libro.precio

        # Crear y guardar la nueva transacción
        transaccion = Transacciones(
            comprador=comprador,
            libro=libro,
            precio=precio,
            estado=estado
        )
        transaccion.save()
        messages.success(request, "¡Transaccion ingresado exitosamente!")
        return redirect('listarTransaccion')  # Redirigir a la lista de transacciones

def listarTransaccion(request):
    transacciones = Transacciones.objects.all()
    return render(request, 'transacciones/listarTransacciones.html', {'transacciones': transacciones})

def editarTransaccion(request, id):
    transaccion= Transacciones.objects.get(id=id)
    libros = Libro.objects.filter(disponible=True)  # Solo libros disponibles
    usuarios_compradores = User.objects.filter(perfil__rol='Comprador')  # Solo compradores

    return render(request, 'transacciones/editarTransacciones.html', {
        'transaccion': transaccion,
        'libros': libros,
        'usuarios_compradores': usuarios_compradores
    })

def actualizarTransaccion(request, id):
    if request.method == 'POST':
        transaccion = Transacciones.objects.get(id=id)

        comprador_id = request.POST.get('comprador')
        libro_id = request.POST.get('libro')
        estado = request.POST.get('estado')

        transaccion.comprador = User.objects.get(id=comprador_id)
        transaccion.libro = Libro.objects.get(id=libro_id)
        transaccion.estado = estado

        transaccion.save()
        messages.success(request, "¡Transaccion editado exitosamente!")
        return redirect('listarTransaccion')  # Redirige al listado de transacciones


def eliminarTransaccion(request, id):
    transaccion = Transacciones.objects.get(id=id)
    transaccion.delete()
    messages.success(request, "¡Transaccion Eliminado exitosamente!")
    return redirect('listarTransaccion')