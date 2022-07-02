from optparse import Values
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import LibroClases, Nota,Asistencia,Observacion,Horario,Alumno,Curso,Profesor,Asignatura, Sala, User,Colegio,Comuna,Apoderado, Arancel, Matricula
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import ContactoForm,NotaForm,ObservacionForm, AsistenciaForm, ColegioForm
#Importando para Serializers
from rest_framework import viewsets
from .serializers import AlumnoSerializer, AsignaturaSerializer, AsistenciaSerializer, HorarioSerializer, CursoSerializer, NotaSerializer, SalaSerializer, UserSerializers
#Para el login (Class User)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#Serializer para la API e IONIC

class UserViewset(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'username': str(request.username),  # `django.contrib.auth.User` instance.
            'password': str(request.password),  # None
        }
        return Response(content)
    queryset = User.objects.all()
    serializer_class = UserSerializers

class AlumnoViewset(viewsets.ModelViewSet):
    queryset= Alumno.objects.all()
    serializer_class=AlumnoSerializer

class HorarioViewset(viewsets.ModelViewSet):
    #queryset=Horario.objects.select_related('rut_profesor').all()
    queryset=Horario.objects.all()
    serializer_class=HorarioSerializer

class AsignaturaViewset(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer

class AsistenciaViewset(viewsets.ModelViewSet):
    queryset=Asistencia.objects.all()
    serializer_class=AsistenciaSerializer

class CursoViewset(viewsets.ModelViewSet):
    queryset=Curso.objects.all()
    serializer_class=CursoSerializer

class NotaViewset(viewsets.ModelViewSet):
    queryset=Nota.objects.all()
    serializer_class=NotaSerializer

class SalaViewset(viewsets.ModelViewSet):
    queryset=Sala.objects.all()
    serializer_class=SalaSerializer

#Comienzo Pagina Web
def index(request):
    return render(request, 'core/index.html')


#creacion de contacto
def contacto(request):
    data = {
        'form': ContactoForm()
    }
    if request.method == 'POST':
        formulario= ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="Mensaje enviado"
        else:
            data["form"] = formulario   
    return render(request, 'core/contacto.html',data)
#Termino de formulario

def ingresar(request):
    rut= request.user.rut_user
    libros=Horario.objects.filter(rut_profesor=rut).select_related('id_curso')
    cargo = request.user.cargo     
    return render(request, 'core/ingresar.html', {'libros': libros, 'cargo':cargo})
   



"""def profesor(user):
    return user.profesor
def alumno(user):
    if user.profesor == False:
        return True"""
        


@login_required
def vistaProfesor(request,id_curso):
    rut= request.user.rut_user 
    notas = Nota.objects.select_related('id_asignatura','rut_alumno__id_curso','rut_profesor').filter(rut_profesor=rut).filter(rut_alumno__id_curso=id_curso)
    observaciones = Observacion.objects.select_related('rut_alumno__id_curso','rut_profesor').filter(rut_profesor=rut).filter(rut_alumno__id_curso=id_curso)
    horarios = Horario.objects.select_related('rut_profesor__id_colegio','id_asignatura','id_sala','id_curso').filter(id_curso=id_curso).filter(rut_profesor=rut)
    asistencias = Asistencia.objects.select_related('rut_alumno__id_curso','rut_profesor').filter(rut_alumno__id_curso=id_curso).filter(rut_profesor=rut)
    return render(request, 'core/vistaProfesor.html', {'notas': notas,  'observaciones': observaciones, 'id_curso': id_curso, 'horarios':horarios, 'asistencias':asistencias})
        

@login_required 
def ingresarNota(request,id_curso):
    rut= request.user.rut_user     
    formulario = NotaForm(request.POST or None)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)  
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request, 'core/ingresarNota.html', {'formulario': formulario, 'alumnos': alumnos,'rut': rut , 'profesor':profesor, 'id_curso': id_curso, 'curso':curso})


@login_required 
def registrarNota(request):
    nota = request.POST['nota']
    tipoevaluacion = request.POST['tipoevaluacion']
    fechaevaluacion = request.POST['fechaevaluacion']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])
    asignatura = Asignatura.objects.get(pk =request.POST['asignatura'])
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    id_curso=request.POST['idlibro'] 

    nota = Nota.objects.create(nota = nota, tipo_evaluacion = tipoevaluacion, fecha_evaluacion = fechaevaluacion, id_libro = idlibro, id_asignatura = asignatura, rut_alumno = rutalumno, rut_profesor = rutprofesor)
    return redirect('vistaProfesor/'+id_curso)


@login_required 
def edicionNota(request,id_curso,id):
    rut= request.user.rut_user     
    id = Nota.objects.get(id_nota = id)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request,"core/edicionNota.html", {"id" : id, "profesor":profesor, "curso":curso,"alumnos":alumnos, 'id_curso': id_curso})


@login_required 
def editarNota(request):
    id_nota = request.POST['id_nota']
    nota = request.POST['nota']
    tipoevaluacion = request.POST['tipoevaluacion']
    fechaevaluacion = request.POST['fechaevaluacion']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])
    asignatura = Asignatura.objects.get(pk =request.POST['asignatura'])
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    id_curso = request.POST['idlibro']
    nuevanota = Nota.objects.get(id_nota = id_nota)
    nuevanota.nota = nota
    nuevanota.tipo_evaluacion = tipoevaluacion
    nuevanota.fecha_evaluacion = fechaevaluacion
    nuevanota.id_libro = idlibro
    nuevanota.id_asignatura = asignatura
    nuevanota.rut_alumno = rutalumno
    nuevanota.rut_profesor = rutprofesor
    nuevanota.save()
    return redirect('/vistaProfesor/'+id_curso)


@login_required 
def eliminarNota(request,id_curso,id):
    nota = Nota.objects.get(id_nota = id)
    nota.delete()
    return redirect('/vistaProfesor/'+id_curso)


@login_required 
def ingresarObservacion(request,id_curso):
    rut= request.user.rut_user     
    formulario = ObservacionForm(request.POST or None)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request, 'core/ingresarObservacion.html', {'formulario': formulario, 'alumnos': alumnos,'rut': rut, 'curso': curso , 'profesor':profesor, 'id_curso':id_curso})




@login_required 
def registrarObservacion(request):
    fechaobservacion = request.POST['fechaobservacion']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])  
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    detalle = request.POST['detalle']
    id_libro = request.POST['idlibro']
    observacion = Observacion.objects.create(fecha_observacion = fechaobservacion,  libro_clases_id_libro = idlibro, rut_alumno = rutalumno, rut_profesor = rutprofesor, detalle = detalle)
    return redirect('/vistaProfesor/'+id_libro)


@login_required 
def edicionObservacion(request,id_curso,id):
    rut= request.user.rut_user     
    id = Observacion.objects.get(id_observacion = id)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request,"core/edicionObservacion.html", {"id" : id, "profesor":profesor, "curso":curso,"alumnos":alumnos, 'id_curso': id_curso})



@login_required 
def editarObservacion(request):
    id_observacion = request.POST['id_observacion']  
    fecha_observacion = request.POST['fechaobservacion']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])  
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    detalle = request.POST['detalle']
    nuevaobservacion= Observacion.objects.get(id_observacion = id_observacion)  
    nuevaobservacion.fecha_observacion = fecha_observacion
    nuevaobservacion.id_libro = idlibro
    nuevaobservacion.rut_alumno = rutalumno
    nuevaobservacion.rut_profesor = rutprofesor
    nuevaobservacion.detalle = detalle
    nuevaobservacion.save()
    id_curso = request.POST['idlibro']
    return redirect('/vistaProfesor/'+id_curso)  


@login_required 
def eliminarObservacion(request,id_curso,id):
    observacion = Observacion.objects.get(id_observacion = id)
    observacion.delete()
    return redirect('/vistaProfesor/'+id_curso)





@login_required 
def ingresarAsistencia(request,id_curso):
    rut= request.user.rut_user     
    formulario = AsistenciaForm(request.POST or None)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)  
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request, 'core/ingresarAsistencia.html', {'formulario': formulario, 'alumnos': alumnos,'rut': rut , 'profesor':profesor, 'id_curso': id_curso, 'curso':curso})


@login_required 
def registrarAsistencia(request):

    fechaasistencia = request.POST['fechaasistencia']
    verificador  = request.POST['verificador']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])
    
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    id_curso=request.POST['idlibro'] 

    asistencia = Asistencia.objects.create(fecha_asistencia = fechaasistencia, verificador=verificador, id_libro = idlibro, rut_alumno = rutalumno, rut_profesor = rutprofesor)
    return redirect('vistaProfesor/'+id_curso)



@login_required 
def edicionAsistencia(request,id_curso,id):
    rut= request.user.rut_user     
    id = Asistencia.objects.get(id_asistencia = id)
    profesor = Profesor.objects.select_related('id_asignatura').filter(rut_profesor=rut)
    alumnos = Alumno.objects.filter(id_curso=id_curso)
    curso = Curso.objects.filter(id_curso=id_curso)
    return render(request,"core/edicionAsistencia.html", {"id" : id, "profesor":profesor, "curso":curso,"alumnos":alumnos, 'id_curso': id_curso})


@login_required 
def editarAsistencia(request):
    id_asistencia = request.POST['id_asistencia']  
    fecha_asistencia = request.POST['fechaasistencia']
    verificador = request.POST['verificador']
    idlibro = LibroClases.objects.get(pk =request.POST['idlibro'])  
    rutalumno = Alumno.objects.get(pk = request.POST['rutalumno'])
    rutprofesor =Profesor.objects.get(pk =request.POST['rutprofesor'])
    
    nuevaasistencia= Asistencia.objects.get(id_asistencia = id_asistencia)  
    
    nuevaasistencia.fecha_asistencia = fecha_asistencia
    nuevaasistencia.verificador = verificador
    nuevaasistencia.id_libro = idlibro
    nuevaasistencia.rut_alumno = rutalumno
    nuevaasistencia.rut_profesor = rutprofesor
    
    nuevaasistencia.save()
    id_curso = request.POST['idlibro']
    return redirect('/vistaProfesor/'+id_curso) 



@login_required 
def eliminarAsistencia(request,id_curso,id):
    asistencia = Asistencia.objects.get(id_asistencia = id)
    asistencia.delete()
    return redirect('/vistaProfesor/'+id_curso)



    
     



@login_required
def vistaAlumno(request):  
    rut= request.user.rut_user         
    notas = Nota.objects.select_related('id_asignatura').select_related('rut_profesor').filter(rut_alumno=rut)
    asistencias = Asistencia.objects.filter(rut_alumno=rut)
    observaciones = Observacion.objects.select_related('rut_profesor').filter(rut_alumno=rut)          
    curso = Alumno.objects.filter(rut_alumno=rut).values_list('id_curso')
    horarios = Horario.objects.select_related('rut_profesor__id_colegio','id_asignatura','id_sala','id_curso').filter(id_curso__in=curso)   
    return render(request, 'core/vistaAlumno.html', {'notas': notas, 'asistencias': asistencias, 'observaciones': observaciones, 'horarios': horarios})

@login_required
def establecimientos(request):  
    #cargo = request.user.cargo        
    establecimientos = Colegio.objects.select_related('id_comuna')
    return render(request, 'core/establecimientos.html', {'establecimientos': establecimientos})

@login_required
def ingresarEstablecimiento(request):
    #rut= request.user.rut_user     
    formulario = ColegioForm(request.POST or None)
    establecimientos = Colegio.objects.select_related('id_comuna')
    comunas = Comuna.objects.all()  
    return render(request, 'core/ingresarEstablecimiento.html', {'formulario': formulario, 'establecimientos':establecimientos,'comunas':comunas})
@login_required 
def registrarEstablecimiento(request):
    
    
    nombrecolegio = request.POST['nombrecolegio']
    telefono = request.POST['telefono']
    direccion = request.POST['direccion']
    idcomuna = Comuna.objects.get(pk =request.POST['idcomuna'])
    
    
    colegio = Colegio.objects.create( nombre = nombrecolegio, telefono = telefono, direccion = direccion, id_comuna = idcomuna)
    return redirect('/establecimientos')


@login_required 
def edicionEstablecimiento(request,id):
        
    id = Colegio.objects.get(id_colegio = id)
    comunas = Comuna.objects.all()
    return render(request,"core/edicionEstablecimiento.html", {"id" : id, "comunas": comunas})


@login_required 
def editarEstablecimiento(request):
    idcolegio = request.POST['idcolegio']  
    nombre = request.POST['nombrecolegio']
    telefono = request.POST['telefono']
    direccion = request.POST['direccion']
    idcomuna =Comuna.objects.get(pk =request.POST['idcomuna'])
    nuevocolegio = Colegio.objects.get(id_colegio = idcolegio)  
    nuevocolegio.nombre = nombre
    nuevocolegio.telefono = telefono
    nuevocolegio.direccion = direccion
    nuevocolegio.id_comuna = idcomuna  
    nuevocolegio.save()
   
    return redirect('/establecimientos')  

@login_required 
def eliminarEstablecimiento(request,id):
    colegio = Colegio.objects.get(id_colegio = id)
    colegio.delete()
    return redirect('/establecimientos')


@login_required
def Profesores(request):  
    colegio= request.user.id_colegio
    profesores = Profesor.objects.filter(id_colegio__nombre=colegio)            
    return render(request, 'core/Profesores.html', {'profesores': profesores})

@login_required
def ingresarProfesor(request):
    
    colegiouser = request.user.id_colegio
    comunas = Comuna.objects.all()
    asignaturas = Asignatura.objects.all()
    colegios= Colegio.objects.filter(nombre=colegiouser)
    return render(request, 'core/ingresarProfesor.html', { 'asignaturas':asignaturas,'comunas':comunas, 'colegios': colegios})

@login_required 
def registrarProfesor(request):
    
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    especialidad = request.POST['especialidad']
    direccion = request.POST['direccion']
    fechacontrato = request.POST['fechacontrato']
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    idasignatura = Asignatura.objects.get(pk = request.POST['idasignatura'])
    
    
    profesor = Profesor.objects.create(rut_profesor = rut,  dv_profesor = dv, p_nombre = pnombre, s_nombre = snombre, ap_paterno = appaterno, ap_materno = apmaterno, especialidad = especialidad, fecha_contrato =fechacontrato, direccion = direccion,
                                            id_comuna=idcomuna,id_colegio=idcolegio,id_asignatura=idasignatura)
    return redirect('/Profesores')


@login_required 
def edicionProfesor(request,id):
        
    id = Profesor.objects.get(rut_profesor = id)
    comunas = Comuna.objects.all()
    asignaturas = Asignatura.objects.all()
    return render(request,"core/edicionProfesor.html", {"id" : id,'comunas':comunas,'asignaturas':asignaturas})


@login_required 
def editarProfesor(request):
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    especialidad = request.POST['especialidad']
    direccion = request.POST['direccion']
    fechacontrato = request.POST['fechacontrato']
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    idasignatura = Asignatura.objects.get(pk = request.POST['idasignatura'])

    nuevoprofesor =Profesor.objects.get(rut_profesor = rut)  

    nuevoprofesor.dv= dv
    nuevoprofesor.p_nombre= pnombre
    nuevoprofesor.s_nombre = snombre
    nuevoprofesor.ap_paterno = appaterno
    nuevoprofesor.ap_materno = apmaterno
    nuevoprofesor.especialidad = especialidad
    nuevoprofesor.direccion = direccion
    nuevoprofesor.fecha_contrato = fechacontrato
    nuevoprofesor.id_comuna = idcomuna
    nuevoprofesor.id_colegio = idcolegio
    nuevoprofesor.id_asignatura = idasignatura
    nuevoprofesor.save()
   
    return redirect('/Profesores')  

@login_required 
def eliminarProfesor(request,id):
    profesor = Profesor.objects.get(rut_profesor = id)
    profesor.delete()
    return redirect('/Profesores')



@login_required
def Apoderados(request):  
    colegio= request.user.id_colegio
    apoderados = Apoderado.objects.filter(id_colegio__nombre=colegio)            
    return render(request, 'core/Apoderados.html', {'apoderados': apoderados})



@login_required
def ingresarApoderado(request):   
    colegiouser = request.user.id_colegio
    comunas = Comuna.objects.all() 
    colegios= Colegio.objects.filter(nombre=colegiouser)
    return render(request, 'core/ingresarApoderado.html', { 'comunas':comunas, 'colegios': colegios})

@login_required 
def registrarApoderado(request):
    
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    telefono = request.POST['telefono']
    direccion = request.POST['direccion']   
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    
    
    
    apoderado = Apoderado.objects.create(rut_apoderado = rut,  dv_apoderado = dv, p_nombre = pnombre, s_nombre = snombre, ap_paterno = appaterno, ap_materno = apmaterno, telefono = telefono,  direccion = direccion,
                                            id_comuna=idcomuna,id_colegio=idcolegio)
    return redirect('/Apoderados')


@login_required 
def edicionApoderado(request,id):
        
    id = Apoderado.objects.get(rut_apoderado = id)
    comunas = Comuna.objects.all()
    
    return render(request,"core/edicionApoderado.html", {"id" : id,'comunas':comunas})


@login_required 
def editarApoderado(request):
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    telefono = request.POST['telefono']
    direccion = request.POST['direccion']
    
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    

    nuevoapoderado =Apoderado.objects.get(rut_apoderado = rut)  

    nuevoapoderado.dv= dv
    nuevoapoderado.p_nombre= pnombre
    nuevoapoderado.s_nombre = snombre
    nuevoapoderado.ap_paterno = appaterno
    nuevoapoderado.ap_materno = apmaterno
    nuevoapoderado.telefono = telefono
    nuevoapoderado.direccion = direccion
    nuevoapoderado.id_comuna = idcomuna
    nuevoapoderado.id_colegio = idcolegio
    
    nuevoapoderado.save()
   
    return redirect('/Apoderados')  


@login_required 
def eliminarApoderado(request,id):
    apoderado = Apoderado.objects.get(rut_apoderado = id)
    apoderado.delete()
    return redirect('/Apoderados')

@login_required
def Alumnos(request):  
    colegio = request.user.id_colegio
    alumnos = Alumno.objects.filter(id_colegio__nombre=colegio)  
        
    return render(request, 'core/Alumnos.html', {'alumnos': alumnos})

@login_required
def ingresarAlumno(request):   
    colegiouser = request.user.id_colegio
    comunas = Comuna.objects.all() 
    colegios= Colegio.objects.filter(nombre=colegiouser)
    apoderados = Apoderado.objects.filter(id_colegio__nombre=colegiouser)
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    return render(request, 'core/ingresarAlumno.html', { 'comunas':comunas, 'colegios': colegios,'apoderados':apoderados,'cursos':cursos})


@login_required 
def registrarAlumno(request):
    
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    fechanac = request.POST['fechanac']
    genero = request.POST['genero']
    direccion = request.POST['direccion']   
    nivelsocio = request.POST['nivelsocio']   
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    idcurso = Curso.objects.get(pk = request.POST['idcurso'])
    rutapoderado = Apoderado.objects.get(pk = request.POST['rutapoderado'])
    
    
    
    apoderado = Alumno.objects.create(rut_alumno = rut,  dv_alumno = dv, p_nombre = pnombre, s_nombre = snombre, ap_paterno = appaterno, ap_materno = apmaterno, fecha_nac = fechanac,  genero = genero,
                                            direccion=direccion,nivel_socio=nivelsocio,id_comuna=idcomuna,id_colegio=idcolegio,id_curso=idcurso,rut_apoderado=rutapoderado)
    return redirect('/Alumnos')


@login_required 
def edicionAlumno(request,id):
    colegiouser = request.user.id_colegio        
    id = Alumno.objects.get(rut_alumno = id)
    colegios= Colegio.objects.filter(nombre=colegiouser)
    apoderados = Apoderado.objects.filter(id_colegio__nombre=colegiouser)
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    comunas = Comuna.objects.all()
    
    return render(request,"core/edicionAlumno.html", {"colegios":colegios,"apoderados":apoderados,"cursos":cursos,"id" : id,'comunas':comunas})

@login_required 
def editarAlumno(request):
    rut = request.POST['rut']
    dv = request.POST['dv']
    pnombre = request.POST['pnombre']
    snombre = request.POST['snombre']
    appaterno = request.POST['appaterno']
    apmaterno = request.POST['apmaterno']
    fechanac = request.POST['fechanac']
    genero = request.POST['genero']
    direccion = request.POST['direccion']
    nivelsocio = request.POST['nivelsocio']
    rutapoderado = Apoderado.objects.get(pk = request.POST['rutapoderado'])
    idcomuna = Comuna.objects.get(pk = request.POST['idcomuna'])
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    idcurso = Curso.objects.get(pk = request.POST['idcurso'])

    nuevoalumno = Alumno.objects.get(rut_alumno = rut)  

    nuevoalumno.dv= dv
    nuevoalumno.p_nombre= pnombre
    nuevoalumno.s_nombre = snombre
    nuevoalumno.ap_paterno = appaterno
    nuevoalumno.ap_materno = apmaterno
    nuevoalumno.genero = genero
    nuevoalumno.direccion = direccion
    nuevoalumno.nivel_socio = nivelsocio
    nuevoalumno.fecha_nac = fechanac
    nuevoalumno.rut_apoderado = rutapoderado
    nuevoalumno.id_comuna = idcomuna
    nuevoalumno.id_colegio = idcolegio
    nuevoalumno.id_curso = idcurso
    nuevoalumno.save()
   
    return redirect('/Alumnos')  

@login_required 
def eliminarAlumno(request,id):
    alumno = Alumno.objects.get(rut_alumno = id)
    alumno.delete()
    return redirect('/Alumnos')


@login_required
def Asignaturas(request):  
    asignaturas = Asignatura.objects.order_by('id_asignatura')       
    return render(request, 'core/Asignaturas.html', {'asignaturas': asignaturas})


@login_required
def ingresarAsignatura(request):   
    
    return render(request, 'core/ingresarAsignatura.html',)


@login_required 
def registrarAsignatura(request):    
    
    nombreasignatura = request.POST['nombreasignatura']
    asignatura = Asignatura.objects.create(nombre = nombreasignatura)
    return redirect('/Asignaturas')

login_required 
def edicionAsignatura(request,id):   
    id = Asignatura.objects.get(id_asignatura = id)
    
    
    return render(request,"core/edicionAsignatura.html", {"id" : id})

@login_required 
def editarAsignatura(request):
    idasignatura = request.POST['idasignatura']  
    nombre = request.POST['nombre']
    nuevaasignatura = Asignatura.objects.get(id_asignatura = idasignatura)  
    nuevaasignatura.nombre = nombre
    nuevaasignatura.save()
   
    return redirect('/Asignaturas')  


@login_required 
def eliminarAsignatura(request,id):
    asignatura = Asignatura.objects.get(id_asignatura = id)
    asignatura.delete()
    return redirect('/Asignaturas')


@login_required
def Salas(request):  
    salas = Sala.objects.order_by('id_sala')       
    return render(request, 'core/Salas.html', {'salas': salas})

@login_required
def ingresarSala(request):
    colegios = Colegio.objects.all()   
    
    return render(request, 'core/ingresarSala.html',{'colegios':colegios})

@login_required 
def registrarSala(request):    
    
    tipo = request.POST['tipo']
    idcolegio = Colegio.objects.get(pk = request.POST['colegio'])
    sala = Sala.objects.create(tipo_sala = tipo,id_colegio=idcolegio)
    return redirect('/Salas')

@login_required 
def edicionSala(request,id):   
    id = Sala.objects.get(id_sala = id)
    colegios = Colegio.objects.all()   
    
    
    return render(request,"core/edicionSala.html", {"id" : id,"colegios":colegios})

@login_required 
def editarSala(request):
    idsala = request.POST['idsala']  
    tipo = request.POST['tipo']
    idcolegio = Colegio.objects.get(pk = request.POST['colegio'])
    nuevasala = Sala.objects.get(id_sala = idsala)  
    nuevasala.tipo_sala = tipo
    nuevasala.id_colegio = idcolegio
    nuevasala.save()
   
    return redirect('/Salas')  

@login_required 
def eliminarSala(request,id):
    sala = Sala.objects.get(id_sala = id)
    sala.delete()
    return redirect('/Salas')

@login_required
def Cursos(request):
    colegiouser = request.user.id_colegio   
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    return render(request, 'core/Cursos.html', {'cursos':cursos})


@login_required
def ingresarCurso(request):   
    colegiouser = request.user.id_colegio   
    colegios= Colegio.objects.filter(nombre=colegiouser)  
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    return render(request, 'core/ingresarCurso.html', {  'colegios': colegios,'cursos':cursos})

@login_required 
def registrarCurso(request):    
    
    grado = request.POST['grado']
    educacion = request.POST['educacion']
    letra = request.POST['letra']
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    curso = Curso.objects.create(grado = grado,educacion=educacion,letra=letra,id_colegio=idcolegio)
    return redirect('/Cursos')

@login_required 
def edicionCurso(request,id):   
    id = Curso.objects.get(id_curso = id)
    colegiouser = request.user.id_colegio   
    colegios= Colegio.objects.filter(nombre=colegiouser)    
    
    
    return render(request,"core/edicionCurso.html", {"id" : id,"colegios":colegios})

@login_required 
def editarCurso(request):
    idcurso = request.POST['idcurso']  
    grado = request.POST['grado']
    educacion = request.POST['educacion']
    letra = request.POST['letra']
    idcolegio = Colegio.objects.get(pk = request.POST['idcolegio'])
    nuevocurso = Curso.objects.get(id_curso = idcurso)  
    nuevocurso.grado = grado
    nuevocurso.educacion = educacion
    nuevocurso.letra = letra
    nuevocurso.id_colegio = idcolegio
    nuevocurso.save()
   
    return redirect('/Cursos')  



@login_required 
def eliminarCurso(request,id):
    curso = Curso.objects.get(id_curso = id)
    curso.delete()
    return redirect('/Cursos')





@login_required
def Horarios(request):
    colegiouser = request.user.id_colegio  
    asignaturas = Asignatura.objects.all() 
    horarios = Horario.objects.filter(id_curso__id_colegio__nombre= colegiouser)
    salas = Sala.objects.filter(id_colegio__nombre=colegiouser)
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    profesores = Profesor.objects.filter(id_colegio__nombre=colegiouser)
    return render(request, 'core/Horarios.html', {'cursos':cursos,'asignaturas':asignaturas,'salas':salas,'cursos':cursos,'profesores':profesores,'horarios':horarios})


@login_required
def ingresarHorario(request):   
    colegiouser = request.user.id_colegio  
    asignaturas = Asignatura.objects.all() 
    horarios = Horario.objects.filter(id_curso__id_colegio__nombre= colegiouser)
    salas = Sala.objects.filter(id_colegio__nombre=colegiouser)
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    profesores = Profesor.objects.filter(id_colegio__nombre=colegiouser)
    return render(request, 'core/ingresarHorario.html', {'cursos':cursos,'asignaturas':asignaturas,'salas':salas,'cursos':cursos,'profesores':profesores,'horarios':horarios})

@login_required 
def registrarHorario(request):    
    dia = request.POST['dia']
    horainicio = request.POST['horainicio']
    horatermino = request.POST['horatermino']
    annio = request.POST['annio']
    asignatura = Asignatura.objects.get(pk = request.POST['asignatura'])
    sala = Sala.objects.get(pk = request.POST['sala'])
    profesor = Profesor.objects.get(pk = request.POST['profesor'])
    curso = Curso.objects.get(pk = request.POST['curso'])
    horario = Horario.objects.create( dia = dia, hora_inicio = horainicio , hora_termino=horatermino, annio=annio,id_asignatura = asignatura, id_sala = sala, rut_profesor = profesor, id_curso = curso)
    return redirect('/Horarios')

@login_required 
def edicionHorario(request,id):   
    id = Horario.objects.get(id_horario = id)
    colegiouser = request.user.id_colegio  
    asignaturas = Asignatura.objects.all() 
    salas = Sala.objects.filter(id_colegio__nombre=colegiouser)
    cursos = Curso.objects.filter(id_colegio__nombre=colegiouser)
    profesores = Profesor.objects.filter(id_colegio__nombre=colegiouser)  
    
    
    return render(request,"core/edicionHorario.html", {"id" : id,'cursos':cursos,'asignaturas':asignaturas,'salas':salas,'cursos':cursos,'profesores':profesores})

@login_required 
def editarHorario(request):
    idhorario = request.POST['idhorario']
    dia = request.POST['dia']
    horainicio = request.POST['horainicio']
    horatermino = request.POST['horatermino']
    annio = request.POST['annio']
    asignatura = Asignatura.objects.get(pk = request.POST['asignatura'])
    sala = Sala.objects.get(pk = request.POST['sala'])
    profesor = Profesor.objects.get(pk = request.POST['profesor'])
    curso = Curso.objects.get(pk = request.POST['curso'])
    nuevohorario = Horario.objects.get(id_horario = idhorario)  
    nuevohorario.dia = dia
    nuevohorario.hora_inicio = horainicio
    nuevohorario.hora_termino = horatermino
    nuevohorario.annio = annio
    nuevohorario.id_asignatura = asignatura
    nuevohorario.id_sala = sala
    nuevohorario.rut_profesor = profesor
    nuevohorario.id_curso = curso
    nuevohorario.save()
   
    return redirect('/Horarios')  

@login_required 
def eliminarHorario(request,id):
    horario = Horario.objects.get(id_horario = id)
    horario.delete()
    return redirect('/Horarios')





@login_required
def Aranceles(request):
    colegiouser = request.user.id_colegio  
    aranceles = Arancel.objects.filter(rut_alumno__id_colegio__nombre=colegiouser).order_by('rut_alumno','id_arancel')
    return render(request, 'core/Aranceles.html', {'aranceles':aranceles})


@login_required
def ingresarArancel(request):   
    colegiouser = request.user.id_colegio   
    alumnos = Alumno.objects.filter(id_colegio__nombre= colegiouser)
    
    return render(request, 'core/ingresarArancel.html', {'alumnos':alumnos})

@login_required 
def registrarArancel(request):    
    
    mes = request.POST['mes']
    valor = request.POST['valor']
    fecha = request.POST['fecha']
    verificador = request.POST['estado']
    rutalumno = Alumno.objects.get(pk = request.POST['alumno'])
    
    arancel = Arancel.objects.create( mes = mes, valor = valor , fecha_limite =fecha, verificador=verificador,rut_alumno = rutalumno)
    return redirect('/Aranceles')

@login_required 
def edicionArancel(request,id):   
    id = Arancel.objects.get(id_arancel = id)
    colegiouser = request.user.id_colegio   
    alumnos = Alumno.objects.filter(id_colegio__nombre= colegiouser)
    
    
    return render(request,"core/edicionArancel.html", {"id" : id,'alumnos':alumnos})

@login_required 
def editarArancel(request):
    idarancel = request.POST['idarancel']
    mes = request.POST['mes']
    valor = request.POST['valor']
    fecha = request.POST['fecha']
    verificador = request.POST['estado']
    rutalumno = Alumno.objects.get(pk = request.POST['alumno'])
    nuevoarancel = Arancel.objects.get(id_arancel = idarancel)  
    nuevoarancel.mes = mes
    nuevoarancel.fecha_limite = fecha
    nuevoarancel.valor = valor
    nuevoarancel.fecha_limite = fecha
    nuevoarancel.verificador = verificador
    nuevoarancel.rut_alumno = rutalumno
    
    nuevoarancel.save()
   
    return redirect('/Aranceles')  

@login_required 
def eliminarArancel(request,id):
    arancel = Arancel.objects.get(id_arancel = id)
    arancel.delete()
    return redirect('/Aranceles')




@login_required
def Matriculas(request):
    colegiouser = request.user.id_colegio  
    matriculas = Matricula.objects.filter(rut_alumno__id_colegio__nombre=colegiouser).order_by('id_matricula')
    return render(request, 'core/Matriculas.html', {'matriculas':matriculas})


@login_required
def ingresarMatricula(request):   
    colegiouser = request.user.id_colegio  
    alumnos = Alumno.objects.filter(id_colegio__nombre= colegiouser)
   
    return render(request, 'core/ingresarMatricula.html', {'alumnos':alumnos })

@login_required 
def registrarMatricula(request):    
    
    fechainicio = request.POST['fechainicio']
    fechatermino = request.POST['fechatermino']
    valor = request.POST['valor']
    pago = request.POST['pago']
    annio = request.POST['annio']
    rutalumno = Alumno.objects.get(pk = request.POST['alumno'])
    
    matricula = Matricula.objects.create( fecha_inicio = fechainicio, fecha_termino = fechatermino,valor = valor , pago =pago,annio=annio,rut_alumno = rutalumno)
    return redirect('/Matriculas')

@login_required 
def edicionMatricula(request,id):   
    id = Matricula.objects.get(id_matricula = id)
    colegiouser = request.user.id_colegio   
    alumnos = Alumno.objects.filter(id_colegio__nombre= colegiouser)
    
    
    return render(request,"core/edicionMatricula.html", {"id" : id,'alumnos':alumnos})

@login_required 
def editarMatricula(request):
    idmatricula = request.POST['idmatricula']
    fechainicio = request.POST['fechainicio']
    fechatermino = request.POST['fechatermino']
    valor = request.POST['valor']
    pago = request.POST['pago']
    annio = request.POST['annio']
    rutalumno = Alumno.objects.get(pk = request.POST['alumno'])
    nuevamatricula = Matricula.objects.get(id_matricula = idmatricula)  
    nuevamatricula.fecha_inicio = fechainicio
    nuevamatricula.fecha_termino = fechatermino
    nuevamatricula.valor = valor
    nuevamatricula.pago = pago
    nuevamatricula.annio = annio
    nuevamatricula.rut_alumno = rutalumno
    
    nuevamatricula.save()
   
    return redirect('/Matriculas')  

@login_required 
def eliminarMatricula(request,id):
    matricula = Matricula.objects.get(id_matricula = id)
    matricula.delete()
    return redirect('/Matriculas')