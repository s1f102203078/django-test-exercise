from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    tasks = Task.objects.all()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)




def delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('index')



def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)
    
    context = {
        'task': task
    }
    return render(request, 'todo/edit.html', context)

def toggle_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed # completed の値を反転させる
    task.save()
    return redirect('index') # 一覧ページに戻る
