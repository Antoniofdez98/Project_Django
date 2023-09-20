from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth import authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Project
from .models import Publication
from .forms import CustomUserCreationForm, UpdateProjectForm, ProjectForm
import requests
import json

# Create your views here.

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            messages.success(request, "Nueva cuenta creada correctamente" )
            return redirect('home')
        else:
            messages.error(request, "Algo ha salido mal - Por favor compruebalo de nuevo")
            return redirect('register')
    return render(request, 'registration/register.html', data)


class ProjectListView(ListView):
    model = Project
    paginate_by = 7
    template_name = 'api/home.html'
    ordering = ['-year']
    def get(self, request, *args, **kwargs):
        project_list = Project.objects.all().order_by('-year')
        buscar = request.GET.get('buscar')
        if buscar:
            project_list = Project.objects.filter(reference__icontains=buscar).order_by('-year')
        paginator = Paginator(project_list, 7)
        page = request.GET.get('page')
        try:
            project_list = paginator.page(page)
        except PageNotAnInteger:
            project_list = paginator.page(1)
        except EmptyPage:
            project_list = paginator.page(paginator.num_pages)
        context = {
            'project_list': project_list
        }
        return render(request, "api/home.html", context)


class ProfileListView(ListView):
    model = Project
    template_name = 'api/profile.html'
    ordering = ['year']

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(
            user=request.user.id).order_by('-year')
        context = {
            'project_list': projects
        }
        return render(request, self.template_name, context)


class PublicationListView(ListView):
    model = Publication
    paginate_by = 5
    template_name = 'api/project.html'
    ordering = ['idScopus']

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs['project'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.kwargs['project']
        context['project_data'] = Project.objects.filter(
            reference=self.kwargs['project'])
        return context


class UpdateProject(UpdateView):
    model = Project
    template_name = 'api/updateproject.html'
    form_class = UpdateProjectForm
    success_url = reverse_lazy('profile')


class CreateProject(CreateView):
    model = Project
    template_name = 'api/createproject.html'
    form_class = ProjectForm
    success_url = reverse_lazy('profile')


class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy('profile')


def get_publication(project, cursor1):

    url = "https://api.elsevier.com/content/search/scopus"
    apiKey = "92bbe03da3e9b6a8a507ed53531823bf"
    query = project
    view = "&view=COMPLETE"
    cursor = cursor1
    headers = {"Content-Type": "application/json", 'X-ELS-APIKey': apiKey}

    r = requests.post(url + "?query=FUND-NO(" + query + ")" +
                      view + "&cursor=" + cursor, headers=headers)

    publication = r.json()
    
    if r.status_code == 401:
        if publication['service-error']['status']['statusCode'] != 'AUTHORIZATION_ERROR':
            cursor = '*'
    else:
        if publication['search-results']['opensearch:totalResults'] != '0':
            cursor_actual = str(publication['search-results']['cursor']['@current'])
            cursor = str(publication['search-results']['cursor']['@next'])
            if 'entry' in publication['search-results']:
                if cursor_actual == '*':
                    clear_data(project)
                for i in publication['search-results']['entry']:
                    publicacion = Publication.objects.create(idScopus=int(i['dc:identifier'][10:]), creator=str(i['dc:creator']), authors=str(i['dc:creator']), title=str(i['dc:title']), year=int(
                        i['prism:coverDisplayDate'][-4:]), source=str(i['source-id']), cited=str(i['citedby-count']), project_id=project, user_id=Project.objects.filter(reference=project).get().user.id, RAW=str(i))
                    publicacion.save()
                for i in publication['search-results']['entry']:
                    referencia = int(i['dc:identifier'][10:])
                    referencia1 = int(Publication.objects.filter(idScopus=referencia).get().idScopus)
                    if referencia == referencia1:
                        if 'prism:doi' in i:
                            Publication.objects.filter(idScopus=referencia).update(doi = str(i['prism:doi']))
                        if 'prism:volume' in i:
                            Publication.objects.filter(idScopus=referencia).update(volume = str(i['prism:volume']))
                        if 'prism:issueIdentifier' in i:
                            Publication.objects.filter(idScopus=referencia).update(issue = str(i['prism:issueIdentifier']))
                    autores1 = ''
                    for j in i['author']:
                        autores1 = autores1 + str(j['authname']) + ', '
                    autores1 = autores1[:-2]
                    Publication.objects.filter(idScopus=referencia).update(authors = autores1)
    return cursor


def clear_data(project):
    Publication.objects.filter(project_id=project).delete()


def UpdatePublications(request, project):
    cursor = '*'
    cursor_before = get_publication(project, cursor)
    if cursor_before != '*':
        while cursor_before != get_publication(project, cursor_before):
            cursor_before = get_publication(project, cursor_before)

    return redirect('project', project)


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'api/publication.html'
