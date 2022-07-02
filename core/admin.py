from re import S
from django.contrib import admin
from core.models import Ciudad,Alumno,Apoderado ,Region,Comuna,Colegio,User,ExamenCono,Curso,Profesor,Asignatura,Arancel,Asistencia,Empleado,Horario,LibroClases,Matricula,Nota,Observacion,Sala,TipoEmp, Contacto
# Register your models here.
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    add_form: CustomUserCreationForm
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Ingrese rut del usuario',
            {
                'fields': (
                                      
                    'rut_user',
                    )
            }
        ),
        (
            'Cargo',
            {
                'fields': (
                                      
                    'cargo',
                    )
            }
        ),
         (
            'Colegio',
            {
                'fields': (
                                      
                    'id_colegio',
                    )
            }
        ),
    )

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display= ('rut_alumno', 'dv_alumno','p_nombre', 'ap_paterno', 'id_curso')
    ordering=('rut_alumno', 'id_curso')
    search_fields= ('rut_alumno', 'p_nombre', 'ap_paterno', 'id_curso')
    list_filter= ('id_curso',)

@admin.register(Apoderado)
class ApoderadoAdmin(admin.ModelAdmin):
    list_display= ('rut_apoderado', 'dv_apoderado','p_nombre', 'ap_paterno', 'id_colegio', 'id_comuna')
    ordering=('rut_apoderado', 'id_colegio')
    search_fields= ('rut_apoderado', 'p_nombre', 'ap_paterno', 'id_colegio', 'id_comuna')
    list_filter= ('id_colegio','rut_apoderado', 'id_comuna')

@admin.register(Arancel)
class ArancelAdmin(admin.ModelAdmin):
    list_display= ('id_arancel', 'mes', 'valor', 'fecha_limite','verificador', 'rut_alumno')
    ordering=('mes', 'id_arancel')
    search_fields= ('id_arancel', 'rut_alumno', 'mes')
    list_filter= ('mes', 'rut_alumno', 'id_arancel')
    list_editable= ('valor',)

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display= ('id_asignatura', 'nombre')
    ordering=('id_asignatura', 'nombre')
    search_fields= ('id_asignatura', 'nombre')
    list_filter= ('id_asignatura', 'nombre')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display= ('id_asistencia', 'rut_alumno','fecha_asistencia', 'id_libro', 'verificador')
    ordering=('fecha_asistencia', 'id_libro', 'id_asistencia')
    search_fields= ('fecha_asistencia', 'rut_alumno', 'id_libro')
    list_filter= ('fecha_asistencia', 'rut_alumno', 'id_libro', 'id_asistencia')
    list_editable= ('fecha_asistencia','verificador')

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display= ('id_ciudad', 'nombre', 'id_region')
    ordering= ('nombre','id_ciudad', 'id_region')
    search_fields= ('id_ciudad', 'nombre', 'id_region')
    list_filter= ('id_ciudad', 'nombre', 'id_region')

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    list_display= ('id_colegio', 'nombre', 'direccion', 'telefono', 'id_comuna')
    ordering= ('id_colegio', 'nombre', 'id_comuna')
    search_fields= ('id_colegio', 'nombre','id_comuna')
    list_filter= ('id_colegio', 'nombre','id_comuna')

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display= ('id_comuna', 'nombre', 'id_ciudad')
    ordering= ('id_comuna', 'nombre', 'id_ciudad')
    search_fields= ('id_comuna', 'nombre', 'id_ciudad')
    list_filter= ('id_comuna', 'nombre', 'id_ciudad'    )

#Verificando como mostrar bien el contacto
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display= ('nombre', 'correo', 'tipo_consulta', 'mensaje')
    ordering= ('nombre', 'tipo_consulta')
    search_fields= ('tipo_consulta', 'correo')
    list_filter= ('tipo_consulta', 'correo')


@admin.register(Curso)
class CursoAdmin (admin.ModelAdmin):
    list_display= ('id_curso', 'grado', 'educacion', 'letra')
    ordering= ('id_curso',)
    search_fields= ('id_curso', 'grado')
    list_filter= ('id_curso',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display= ('rut_emp', 'dv_emp', 'p_nombre', 'ap_paterno',  'id_colegio')
    ordering= ('fecha_contrato', 'rut_emp', 'id_colegio')
    search_fields= ('rut_emp','id_tipo_emp', 'id_colegio')
    list_filter= ('rut_emp','id_tipo_emp', 'id_colegio', 'id_comuna')
    #list_editable= ('fecha_contrato',)

@admin.register(ExamenCono)
class ExamenConoAdmin(admin.ModelAdmin):
    list_display= ('id_examenenes', 'fecha_rendicion', 'lenguaje', 'matematica')
    ordering= ('fecha_rendicion', 'id_examenenes')
    search_fields= ('id_examenenes','lenguaje', 'matematica')
    list_filter= ('id_examenenes', 'fecha_rendicion', 'lenguaje', 'matematica')
    
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display= ('id_asignatura', 'dia', 'hora_inicio', 'hora_termino', 'id_sala', 'id_curso')
    ordering= ('dia', 'id_asignatura')
    search_fields= ('dia', 'id_asignatura', 'id_sala', 'id_curso')
    list_filter= ('dia', 'id_curso', 'id_asignatura')

@admin.register(LibroClases)
class LibroClasesAdmin(admin.ModelAdmin):
    list_display= ('id_curso', 'annio_escolar')
    ordering= ('id_curso', 'annio_escolar')
    search_fields= ('id_curso', 'annio_escolar')
    list_filter= ('id_curso', 'annio_escolar')

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display= ('id_matricula', 'rut_alumno', 'valor', 'pago', 'fecha_inicio', 'fecha_termino')
    ordering= ('fecha_inicio', 'id_matricula')
    search_fields= ('rut_alumno', 'id_matricula', 'pago')
    list_filter= ('id_matricula', 'rut_alumno')
    list_editable= ('valor', 'pago')

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display= ('rut_alumno', 'nota', 'tipo_evaluacion', 'fecha_evaluacion', 'id_asignatura', 'rut_profesor', 'id_libro')
    ordering= ('rut_alumno', 'nota', 'tipo_evaluacion','id_asignatura','id_libro')
    search_fields= ('rut_alumno','id_asignatura', 'id_libro','tipo_evaluacion','fecha_evaluacion' )
    list_filter= ('id_libro','id_asignatura','tipo_evaluacion','fecha_evaluacion','rut_alumno')

@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display= ('id_observacion', 'rut_profesor', 'libro_clases_id_libro', 'rut_alumno', 'fecha_observacion', 'detalle')
    ordering= ('id_observacion', 'libro_clases_id_libro','fecha_observacion' )
    search_fields= ('rut_alumno', 'id_observacion', 'fecha_observacion')
    list_filter= ('id_observacion', 'rut_profesor', 'libro_clases_id_libro', 'rut_alumno', 'fecha_observacion')
    list_editable= ('fecha_observacion', 'detalle')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display= ('rut_profesor', 'dv_profesor', 'p_nombre', 'ap_paterno', 'id_asignatura','especialidad', 'fecha_contrato', 'id_colegio', 'direccion')
    ordering= ('id_colegio', 'id_asignatura','especialidad', 'rut_profesor')
    search_fields= ('rut_profesor', 'id_colegio', 'id_asignatura','especialidad', 'comuna')
    list_filter= ('id_colegio', 'id_asignatura', 'especialidad', 'fecha_contrato')
    list_editable= ('id_colegio', 'direccion')

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display= ('id_region', 'nombre')
    ordering= ('id_region', 'nombre')
    search_fields= ('id_region', 'nombre')
    list_filter= ('id_region', 'nombre')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display= ('id_sala', 'tipo_sala', 'id_colegio')
    ordering= ('id_colegio', 'id_sala', 'tipo_sala')
    search_fields= ('id_sala', 'tipo_sala', 'id_colegio')
    list_filter= ('id_sala', 'tipo_sala', 'id_colegio')

#Agregar datos para la tabla TipoEmp
@admin.register(TipoEmp)
class TipoEmpAdmin(admin.ModelAdmin):
    list_display= ('id_tipo_emp', 'nombre_tipo_emp')
    ordering= ('id_tipo_emp', 'nombre_tipo_emp')
    search_fields= ('id_tipo_emp', 'nombre_tipo_emp')
    list_filter= ('id_tipo_emp', 'nombre_tipo_emp')

#En caso de error con al tabla User, comentar esta clase y quitar comentario en (User, CustomUserAdmin)
"""@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display= ('username', 'profesor')
    ordering= ('rut_user',)
    search_fields= ('rut_user',)
    list_filter= ('rut_user',)
"""
""" Comentado por si existe algun error y debamos recuperar las vistas """

#admin.site.register(Alumno)
#admin.site.register(Ciudad)
#admin.site.register(Apoderado)
#admin.site.register(Region)
#admin.site.register(Comuna)
#admin.site.register(Colegio)

admin.site.register(User, CustomUserAdmin)

#admin.site.register(ExamenCono)
#admin.site.register(Curso)
#admin.site.register(Profesor)
#admin.site.register(Asignatura)
#admin.site.register(Arancel)
#admin.site.register(Asistencia)
#admin.site.register(Empleado)
#admin.site.register(Horario)
#admin.site.register(LibroClases)
#admin.site.register(Matricula)
#admin.site.register(Nota)
#admin.site.register(Observacion)
#admin.site.register(Sala)
#admin.site.register(TipoEmp)

#Registrando el contacto
#admin.site.register(Contacto)

