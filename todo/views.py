from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class CustomLoginView(LoginView):
    template_name="todo/login.html"
    fields="__all__"
    redirect_authenticated_user= True
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class RegisterView(FormView):
    template_name="todo/register.html"
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterView,self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


class Task_list(LoginRequiredMixin,ListView):
   model=Task 
   context_object_name='tasks'

   def get_context_data(self, **kwargs):
       context= super().get_context_data(**kwargs)
       context['tasks']=context['tasks'].filter(user=self.request.user)
       context['count']=context['tasks'].filter(complete=False).count()
       search_input = self.request.GET.get('search-area') or ''
       if search_input:
           context['tasks'] = context['tasks'].filter(
               title__contains=search_input)
           context['search_input'] = search_input
       return context

class Task_Detail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'


class Task_Create(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self, form) :
        form.instance.user=self.request.user
        return super(Task_Create,self).form_valid(form)

class Task_Update(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))