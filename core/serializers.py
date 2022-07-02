
#Librerias 
from dataclasses import field, fields
from .models import Alumno, Asignatura, Asistencia, Horario, Curso, Nota, Sala, User
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Alumno
        fields= '__all__'
        #fields=('p_nombre','ap_paterno', 'rut_alumno', 'dv_alumno', 'direccion')

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Horario
        fields= '__all__'
        #exclude = ['id_horario', 'annio']

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asignatura
        fields='__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asistencia
        fields= '__all__'
        #exclude = ['id_libro', 'rut_alumno']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Curso
        fields= '__all__'
        #exclude = ['id_curso', 'grado', '']

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nota
        fields= '__all__'
        #fields = ('nota','tipo_evaluacion')

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sala
        fields= '__all__'
        #exclude = ['id_colegio']
        
