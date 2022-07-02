from django.db import router

from core.serializers import NotaSerializer
from .views import  *
from django.urls import path, include
from rest_framework import routers

#Direcionnes API

router = routers.DefaultRouter()
router.register('alumno', AlumnoViewset)
router.register('horario', HorarioViewset)
router.register('asignatura', AsignaturaViewset)
router.register('asistencia', AsistenciaViewset)
router.register('curso', CursoViewset)
router.register('nota', NotaViewset)
router.register('sala', SalaViewset)
router.register('login', UserViewset)

#Probar funcionamientos del API y JSON localhost:8000/api/ 

urlpatterns = [
    path('', index), 
    path('contacto', contacto),
    path('vistaAlumno', vistaAlumno, name='vistaAlumno'),
    path('vistaProfesor/<id_curso>', vistaProfesor, name='vistaProfesor'), 
    path('ingresar', ingresar),
    path('vistaProfesor/<id_curso>/ingresarNota',ingresarNota, name ='ingresarNota'),
    path('registrarNota', registrarNota),
    path('vistaProfesor/<id_curso>/edicionNota/<id>', edicionNota),
    path('editarNota', editarNota),
    path('vistaProfesor/<id_curso>/eliminarNota/<id>', eliminarNota),
    path('vistaProfesor/<id_curso>/ingresarObservacion', ingresarObservacion, name ='ingresarObservacion'),
    path('registrarObservacion', registrarObservacion),
    path('vistaProfesor/<id_curso>/edicionObservacion/<id>', edicionObservacion),
    path('editarObservacion', editarObservacion),
    path('vistaProfesor/<id_curso>/eliminarObservacion/<id>', eliminarObservacion),
    path('vistaProfesor/<id_curso>/ingresarAsistencia', ingresarAsistencia, name ='ingresarAsistencia'),
    path('registrarAsistencia', registrarAsistencia),
    path('vistaProfesor/<id_curso>/edicionAsistencia/<id>', edicionAsistencia),
    path('editarAsistencia', editarAsistencia),
    path('vistaProfesor/<id_curso>/eliminarAsistencia/<id>', eliminarAsistencia),
    path('establecimientos', establecimientos,name ='establecimientos'),
    path('establecimientos/ingresarEstablecimiento', ingresarEstablecimiento, name ='ingresarEstablecimiento'),
    path('registrarEstablecimiento', registrarEstablecimiento),
    path('establecimientos/edicionEstablecimiento/<id>', edicionEstablecimiento),
    path('editarEstablecimiento', editarEstablecimiento),
    path('establecimientos/eliminarEstablecimiento/<id>', eliminarEstablecimiento),
    path('Profesores', Profesores, name='Profesores'),
    path('ingresarProfesor', ingresarProfesor, name='ingresarProfesor'),
    path('registrarProfesor', registrarProfesor, name='registrarProfesor'),
    path('Profesores/edicionProfesor/<id>', edicionProfesor),
    path('editarProfesor', editarProfesor),
    path('Profesores/eliminarProfesor/<id>', eliminarProfesor),
    path('Apoderados', Apoderados, name='Apoderados'),
    path('ingresarApoderado', ingresarApoderado, name='ingresarApoderado'),
    path('registrarApoderado', registrarApoderado, name='registrarApoderado'),
    path('Apoderados/edicionApoderado/<id>', edicionApoderado),
    path('editarApoderado', editarApoderado),
    path('Apoderados/eliminarApoderado/<id>', eliminarApoderado),
    path('Alumnos', Alumnos, name='Alumnos'),
    path('ingresarAlumno', ingresarAlumno, name='ingresarAlumno'),
    path('registrarAlumno', registrarAlumno, name='registrarAlumno'),
    path('Alumnos/edicionAlumno/<id>', edicionAlumno),
    path('editarAlumno', editarAlumno), 
    path('Alumnos/eliminarAlumno/<id>', eliminarAlumno),
    path('Asignaturas', Asignaturas, name='Asignaturas'),
    path('ingresarAsignatura', ingresarAsignatura, name='ingresarAsignatura'),
    path('registrarAsignatura', registrarAsignatura, name='registrarAsignatura'),
    path('Asignaturas/edicionAsignatura/<id>', edicionAsignatura),
    path('editarAsignatura', editarAsignatura), 
    path('Asignaturas/eliminarAsignatura/<id>', eliminarAsignatura),
    path('Salas', Salas, name='Salas'),
    path('ingresarSala', ingresarSala, name='ingresarSala'),
    path('registrarSala', registrarSala, name='registrarSala'),
    path('Salas/edicionSala/<id>', edicionSala), 
    path('editarSala', editarSala),
    path('Salas/eliminarSala/<id>', eliminarSala),
    path('Cursos', Cursos, name='Cursos'),
    path('ingresarCurso', ingresarCurso, name='ingresarCurso'),
    path('registrarCurso', registrarCurso, name='registrarCurso'),
    path('Cursos/edicionCurso/<id>', edicionCurso), 
    path('editarCurso', editarCurso),
    path('Cursos/eliminarCurso/<id>', eliminarCurso),
    path('Horarios', Horarios, name='Horarios'),
    path('ingresarHorario', ingresarHorario, name='ingresarHorario'),
    path('registrarHorario', registrarHorario, name='registrarHorario'),
    path('Horarios/edicionHorario/<id>', edicionHorario), 
    path('editarHorario', editarHorario),
    path('Horarios/eliminarHorario/<id>', eliminarHorario),
    path('Aranceles', Aranceles, name='Aranceles'),
    path('ingresarArancel', ingresarArancel, name='ingresarArancel'),
    path('registrarArancel', registrarArancel, name='registrarArancel'),
    path('Aranceles/edicionArancel/<id>', edicionArancel), 
    path('editarArancel', editarArancel),
    path('Aranceles/eliminarArancel/<id>', eliminarArancel),
    path('Matriculas', Matriculas, name='Matriculas'),
    path('ingresarMatricula', ingresarMatricula, name='ingresarMatricula'),
    path('registrarMatricula', registrarMatricula, name='registrarMatricula'),
    path('Matriculas/edicionMatricula/<id>', edicionMatricula), 
    path('editarMatricula', editarMatricula),
    path('Matriculas/eliminarMatricula/<id>', eliminarMatricula),
    
    path('api/', include(router.urls)), 
]