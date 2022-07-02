from sys import maxsize
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
cargos = [
    [0, "Sostenedor"],
    [1, "Director"],
    [2, "Subdirector Academico"],
    [4, "Subdirector Administrativo y Finanzas"],
    [5, "Asistente de Admision y Matriculas"],
    [6, "Asistente de Administracion y Finanzas"],
    [7, "Profesor"],
    [8, "Alumno"],
]

class User(AbstractUser):  
    rut_user = models.IntegerField(null=True) 
    cargo = models.IntegerField(choices=cargos,null=True)
    id_colegio = models.ForeignKey('Colegio', models.DO_NOTHING, db_column='id_colegio', null=True,verbose_name="Colegio")

class Alumno(models.Model):
    rut_alumno = models.IntegerField(primary_key=True, verbose_name='Rut')
    dv_alumno = models.CharField(max_length=1, verbose_name='DV')
    p_nombre = models.CharField(max_length=15 , verbose_name = "Primer nombre")
    s_nombre = models.CharField(max_length=15, blank=True, null=True)
    ap_paterno = models.CharField(max_length=15)
    ap_materno = models.CharField(max_length=15, blank=True, null=True)
    fecha_nac = models.DateField()
    genero = models.CharField(max_length=1)
    direccion = models.CharField(max_length=25, blank=True, null=True)
    nivel_socio = models.CharField(max_length=10)
    id_examenes = models.OneToOneField('ExamenCono', models.DO_NOTHING, db_column='id_examenes',null=True)
    rut_apoderado = models.ForeignKey('Apoderado', models.DO_NOTHING, db_column='rut_apoderado')
    id_colegio = models.ForeignKey('Colegio', models.DO_NOTHING, db_column='id_colegio')
    id_curso = models.ForeignKey('Curso', models.DO_NOTHING, db_column='id_curso', verbose_name='Curso')
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')

    def __str__(self):
        return f"{self.rut_alumno , self.p_nombre , self.ap_paterno}"
    class Meta:
        managed = True
        db_table = 'alumno'
        verbose_name_plural = 'Alumnos'
        


class Apoderado(models.Model):
    rut_apoderado = models.IntegerField(primary_key=True)
    dv_apoderado = models.CharField(max_length=1, verbose_name='DV')
    p_nombre = models.CharField(max_length=15)
    s_nombre = models.CharField(max_length=15)
    ap_paterno = models.CharField(max_length=15)
    ap_materno = models.CharField(max_length=15)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=25)
    id_colegio = models.ForeignKey('Colegio', models.DO_NOTHING, db_column='id_colegio')
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        managed = True
        db_table = 'apoderado'
        verbose_name_plural = 'Apoderados'

class Arancel(models.Model):
    id_arancel = models.AutoField(primary_key=True)
    mes = models.CharField(max_length=10)
    valor = models.FloatField()
    fecha_limite = models.DateField()
    verificador = models.CharField(max_length=1)
    rut_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='rut_alumno')

    class Meta:
        managed = True
        db_table = 'arancel'
        verbose_name_plural = 'Aranceles'


class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True, verbose_name='ID')
    nombre = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        managed = True
        db_table = 'asignatura'
        verbose_name_plural = 'Asignaturas'


class Ciudad(models.Model):
    id_ciudad = models.AutoField(primary_key=True, verbose_name='Ciudad')
    nombre = models.CharField(max_length=35)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region', verbose_name='Region')

    def __str__(self):
        return f"{self.nombre }"

    class Meta:
        managed = True
        db_table = 'ciudad'
        verbose_name_plural = 'Ciudades'


class Colegio(models.Model):
    id_colegio = models.AutoField(primary_key=True, verbose_name= "ID ")
    nombre = models.CharField(max_length=20)
    telefono = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=25)
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')

    def __str__(self):
        return f"{self.nombre }"

    class Meta:
        managed = True
        db_table = 'colegio'
        verbose_name_plural = 'Colegios'


class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    id_ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, db_column='id_ciudad')

    def __str__(self):
        return f"{self.nombre }"

    class Meta:
        managed = True
        db_table = 'comuna'
        verbose_name_plural = 'Comunas'


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=1)
    educacion = models.CharField(max_length=10)
    letra = models.CharField(max_length=1)
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio')
    rut_profesor = models.OneToOneField('Profesor', models.DO_NOTHING, db_column='rut_profesor',null=True)

    def __str__(self):
        return f"{self.grado + ' ' + self.educacion + ' ' + self.letra}"

    class Meta:
        managed = True
        db_table = 'curso'
        verbose_name_plural = 'Cursos'


class Empleado(models.Model):
    rut_emp = models.IntegerField(primary_key=True, verbose_name='Rut')
    dv_emp = models.CharField(max_length=1, verbose_name='Digito Verificador')
    p_nombre = models.CharField(max_length=15, verbose_name='Primer Nombre')
    s_nombre = models.CharField(max_length=15, blank=True, null=True, verbose_name='Segundo Nombre')
    ap_paterno = models.CharField(max_length=15, verbose_name='Apellido Paterno')
    ap_materno = models.CharField(max_length=15, blank=True, null=True, verbose_name='Apellido Materno')
    direccion = models.CharField(max_length=50, blank=True, null=True, verbose_name='Direccion')
    fecha_contrato = models.DateField()
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', verbose_name='Colegio')
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna', verbose_name='Comuna')
    id_tipo_emp = models.ForeignKey('TipoEmp', models.DO_NOTHING, db_column='id_tipo_emp', blank=True, null=True, verbose_name='Tipo de Empleado')

    class Meta:
        managed = True
        db_table = 'empleado'
        verbose_name_plural = 'Empleados'


class ExamenCono(models.Model):
    id_examenenes = models.AutoField(primary_key=True)
    fecha_rendicion = models.DateField()
    lenguaje = models.IntegerField()
    matematica = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'examen_cono'
        verbose_name_plural = 'Examen de Diagnostico'


class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=10)
    hora_inicio = models.CharField(max_length=5)
    hora_termino = models.CharField(max_length=5)
    annio = models.IntegerField()
    id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asignatura')
    id_sala = models.ForeignKey('Sala', models.DO_NOTHING, db_column='id_sala')
    rut_profesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='rut_profesor')
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso')

    class Meta:
        managed = True
        db_table = 'horario'
        verbose_name_plural = 'Horarios'
        


class LibroClases(models.Model):
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso',primary_key=True)
    annio_escolar = models.IntegerField(verbose_name='Año')
    
    

    class Meta:
        managed = True
        db_table = 'libro_clases'
        verbose_name_plural = 'Libros de Clases'


class Matricula(models.Model):
    id_matricula = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    valor = models.IntegerField()
    pago = models.CharField(max_length=1)
    annio = models.IntegerField(null = True)
    rut_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='rut_alumno')

    class Meta:
        managed = True
        db_table = 'matricula'
        verbose_name_plural = 'Matriculas'


class Observacion(models.Model):
    id_observacion = models.AutoField(primary_key=True)
    fecha_observacion = models.DateTimeField()
    detalle = models.CharField(max_length=255, blank=True, null=True)
    libro_clases_id_libro = models.ForeignKey(LibroClases, models.DO_NOTHING, db_column='libro_clases_id_libro')
    rut_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='rut_alumno')
    rut_profesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='rut_profesor', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'observacion'
        verbose_name_plural = 'Observaciones'


class Profesor(models.Model):
    rut_profesor = models.IntegerField(primary_key=True)
    dv_profesor = models.CharField(max_length=1, verbose_name='DV')
    p_nombre = models.CharField(max_length=15, verbose_name='Nombre')
    s_nombre = models.CharField(max_length=15, blank=True, null=True)
    ap_paterno = models.CharField(max_length=15, verbose_name='Apellido')
    ap_materno = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=35)
    fecha_contrato = models.DateField()
    direccion = models.CharField(max_length=25)
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', blank=True, null=False)
    id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asignatura', verbose_name='Asignatura')
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        managed = True
        db_table = 'profesor'
        verbose_name_plural = 'Profesores'

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    fecha_asistencia = models.DateField()
    verificador = models.CharField(max_length=10)
    id_libro = models.ForeignKey('LibroClases', models.DO_NOTHING, db_column='id_libro')
    rut_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='rut_alumno')
    rut_profesor = models.ForeignKey(Profesor, models.DO_NOTHING, db_column='rut_profesor')

    class Meta:
        managed = True
        db_table = 'asistencia'
        verbose_name_plural = 'Asistencias'

class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    nota = models.FloatField()
    tipo_evaluacion = models.CharField(max_length=15)
    fecha_evaluacion = models.DateField()
    id_libro = models.ForeignKey(LibroClases, models.DO_NOTHING, db_column='id_libro')
    id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asignatura', verbose_name='Asignatura')
    rut_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='rut_alumno',verbose_name='Alumno')
    rut_profesor = models.ForeignKey(Profesor, models.DO_NOTHING, db_column='rut_profesor',verbose_name='Profesor')
    

    
    class Meta:
        managed = True
        db_table = 'nota'
        verbose_name_plural = 'Notas'

class Region(models.Model):
    id_region = models.IntegerField(primary_key=True, verbose_name='Region Nro')
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre }"

    class Meta:
        managed = True
        db_table = 'region'
        verbose_name_plural = 'Regiones'


class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    tipo_sala = models.CharField(max_length=15)
    id_colegio = models.ForeignKey(Colegio, models.DO_NOTHING, db_column='id_colegio', verbose_name='Colegio')


    class Meta:
        managed = True
        db_table = 'sala'
        verbose_name_plural = 'Salas'


class TipoEmp(models.Model):
    id_tipo_emp = models.IntegerField(primary_key=True)
    nombre_tipo_emp = models.CharField(max_length=15)

    class Meta:
        managed = True
        db_table = 'tipo_emp'
        verbose_name_plural = 'Tipo de Empleado'

#Modelo de Contacto

opciones_consulta = [
    [0, "Problemas de Login"],
    [1, "Consultas Generales"],
    [2, "Consultas Administrativas/Financiamiento"],
    [3, "Otros"],
]

class Contacto(models.Model):
    nombre=models.CharField(max_length=50)
    
    correo=models.EmailField()
    tipo_consulta=models.IntegerField(choices=opciones_consulta)
    mensaje=models.TextField()
    
    class Meta:
        managed = True
        db_table = 'Contacto'
        verbose_name_plural = 'Contactos'

def __str__(self):
    return self.nombre