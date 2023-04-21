from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

# importing ability to block screens until logged in
from django.contrib.auth.mixins import LoginRequiredMixin

# used to create user
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

from .models import Task

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # redirecting user after registering account
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # making sure logged in users can't view register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


# name of first view

# LoginRequiredMixin means that user cannot access main list screen without logging in


class TaskList(LoginRequiredMixin, ListView):
    model = Task

    # changing 'object_list' (django default name) to 'tasks'
    context_object_name = 'tasks'

    # showing only logged in user's tasks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # adding search bar functionality
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # search for requested text anywhere in the tasks
            # title__startswith is used to search from begining of the tasks name
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task

    # removing field for username input
    fields = ['title', 'description', 'complete']

    # once item creace redirects user back to list
    success_url = reverse_lazy('tasks')

    # making username field auto fill to logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
