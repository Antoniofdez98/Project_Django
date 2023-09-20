from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UpdateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['year', 'convocatory', 'area', 'subarea', 'title', 'cif', 'ccaa', 'city', 'money', 'user']
        labels = {
            'year': 'Año',
            'convocatory': 'Convocatoria',
            'area': 'Área',
            'subarea': 'Subárea',
            'title': 'Título',
            'cif': 'C.I.F.',
            'ccaa': 'Comunidad Autónoma',
            'city': 'Provincia',
            'money': '€ Conc.'
        }
        widgets = {
            'year': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            'convocatory': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'area': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'subarea': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'title': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'cif': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'ccaa': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'city': forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'money': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                }
            )
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['user', 'reference', 'year', 'convocatory', 'area', 'subarea', 'title', 'cif', 'ccaa', 'city', 'money']
        labels = {
            'user': 'Id del usuario',
            'reference': 'Referencia',
            'year': 'Año',
            'convocatory': 'Convocatoria',
            'area': 'Área',
            'subarea': 'Subárea',
            'title': 'Título',
            'cif': 'C.I.F.',
            'ccaa': 'Comunidad Autónoma',
            'city': 'Provincia',
            'money': '€ Conc.'
        }
        widgets = {
            'reference': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Código de Referencia',
                }
            ),
            'year': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            'convocatory': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Convocatoria'
                }
            ),
            'area': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Área'
                }
            ),
            'subarea': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Subárea'
                }
            ),
            'title': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Título'
                }
            ),
            'cif': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'CIF'
                }
            ),
            'ccaa': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Comunidad Autónoma'
                }
            ),
            'city': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder': 'Provincia'
                }
            ),
            'money': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                }
            )
        }


