from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.login_usuario),
    path('index/', views.index, name='index'), 
    
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    path('libros/', views.listar_libros, name='listarLibros'),
    
    path('detalle/detalles_libro/<int:id>/', views.detalles_libro, name='detalles_libro'),
    
    path('Usuario/registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('Usuario/listar/', views.listar_usuarios, name='listar_usuarios'),
    path('Usuario/editarUsuario/<int:id>/', views.editarUsuario, name='editarUsuario'),
    path('procesarEdisionUsuario/', views.procesarEdisionUsuario, name='procesar_edision_usuario'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    
    path('login/', views.login_usuario, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'), 
    
    path('Categoria/agregarCategoria/', views.agregarCategoria, name='agregarCategoria'),
    path('Categoria/guardarCategoria/', views.guardarCategoria, name='guardarCategoria'),
    path('Categoria/listarCategoria/', views.listarCategoria, name='listarCategoria'),
    path('eliminarCategoria/<int:id>/', views.eliminarCategoria, name='eliminarCategoria'),
    
    path('libro/agregarLibro/', views.agregarLibro, name='agregarLibro'),
    path('libro/guardarLibro/', views.guardarLibro, name='guardarLibro'),
    path('libro/listarLibro/', views.listarLibro, name='listarLibro'),
    path('libro/editarLibro/<int:id>/', views.editarLibro, name='editarLibro'),
    path('actualizarLibro/<int:id>/', views.actualizarLibro, name='actualizarLibro'),
    path('eliminarLibro/<int:id>/', views.eliminarLibro, name='eliminarLibro'),
    
    
    path('transacciones/agregarTransaccion/', views.agregarTransaccion, name='agregarTransaccion'),
    path('transacciones/guardarTransaccion/', views.guardarTransaccion, name='guardarTransaccion'),
    path('transacciones/listarTransaccion/', views.listarTransaccion, name='listarTransaccion'),
    path('transacciones/editarTransaccion/<int:id>/', views.editarTransaccion, name='editarTransaccion'),
    path('actualizarTransaccion/<int:id>/', views.actualizarTransaccion, name='actualizarTransaccion'),

    path('eliminarTransaccion/<int:id>/', views.eliminarTransaccion, name='eliminarTransaccion'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
