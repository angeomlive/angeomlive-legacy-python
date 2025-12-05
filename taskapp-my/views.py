# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import Context
from .models import TaskSection, Task, TaskType1, TaskType2, TaskType2Variant
from random import randint


def context_base():
    context = Context({})
    context['title'] = 'Аналитическая геометрия'
    context['subtitle'] = 'Проверь свои знания по курсу аналитической геометрии'
    return context


def view_taskapp_main_page(request):
    context = context_base()
    context['sections'] = TaskSection.objects.all()
    return render(request, "taskapp/main-page.html", context)


def view_task_solo(request, number):

    context = context_base()
    context['subtitle'] = str(Task.objects.get(number=number).section.name) + ': вопрос №'+str(number)
    template = ''

    template, context = task(request, template, context, number)

    return render(request, template, context)


def view_task_solo_random(request, section):
    context = context_base()
    template = ''

    if request.method == 'POST':
        number = request.POST['task_number']
    else:
        max_num = Task.objects.filter(published=True, section=TaskSection.objects.get(slug=section)).count()
        rand = randint(0, max_num - 1)
        number = Task.objects.filter(published=True, section=TaskSection.objects.get(slug=section))[rand].number
    context['subtitle'] = str(Task.objects.get(number=number).section.name)
    template, context = task(request, template, context, number)

    return render(request, template, context)


def task(request, template, context, number):
    pass
    print(template)
    task_option = Task.objects.get(number=number)
    context['task_option'] = task_option

    if task_option.type.id == 1:
        task = TaskType1.objects.get(pk=task_option.id_inclass)
        context['task'] = task

        if request.method == 'POST':
            template = 'taskapp/task-type1-result.html'
        else:
            template = 'taskapp/task-type1.html'

    elif task_option.type.id == 2:
        task = TaskType2.objects.get(pk=task_option.id_inclass)
        context['task'] = task
        context['task_variants'] = TaskType2Variant.objects.filter(task=task)

        if request.method == 'POST':
            context['choice_id'] = int(request.POST['choice'])
            template = 'taskapp/task-type2-result.html'
        else:
            template = 'taskapp/task-type2.html'

    return template, context









def test_edt_task(request):
    context = context_base()
    context['sections'] = TaskSection.objects.all()
    return render(request, "test/test.html", context)


def test(request):
    context = context_base()
    context['sections'] = TaskSection.objects.all()
    if request.method == "POST":
        form = TaskType1Form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False, image=request.FILES['image'])
            post.save()
            context['task'] = TaskType1.objects.get(pk=post.pk)
            return render(request, "test/test-ok.html", context)
    else:
        form = TaskType1Form()
        context['form'] = form

    return render(request, "test/test.html", context)
