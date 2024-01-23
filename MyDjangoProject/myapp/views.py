from django.shortcuts import render
from .models import Task,UserProfile
from django.shortcuts import render, get_object_or_404,redirect
from .forms import TaskForm
from .forms import UserProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Q


# @login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'myapp/profile.html', {'form': form})


def task_list(request):
    # query = request.GET.get('q')
    # tasks = Task.objects.all()

    # if query:
    #     tasks = tasks.filter(
    #         Q(title__icontains=query) | Q(description__icontains=query)
    #     )

    # return render(request, 'myapp/task_list.html', {'tasks': tasks})
    task_list = Task.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(task_list, 10)  # Show 10 tasks per page

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'myapp/task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'myapp/task_detail.html', {'task': task})

# @login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'myapp/task_form.html', {'form': form})

# @login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/task_form.html', {'form': form})

def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

# @user_passes_test(lambda u: u.groups.filter(name='Administrators').exists())
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'myapp/task_delete.html', {'task': task})