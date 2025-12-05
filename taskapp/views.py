# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import Context
from .models import  Task, TaskType1, TaskType2, TaskType2Variant, TaskSection
from random import randint
import datetime

def context_base():
    context = Context({})
    context['title'] = 'Аналитическая геометрия'
    context['subtitle'] = 'Проверь свои знания по курсу аналитической геометрии'
    context['date'] = datetime.datetime.now().year
    return context


def view_taskapp_main_page(request):
    context = context_base()
    context['sections'] = TaskSection.objects.filter(published=True, ).order_by('custom_view_rank')

    request.session['task'] = {}
    request.session['task'][-159] = 0
    request.session['task'][-259] = 1

    return render(request, "taskapp/taskapp-main-page.html", context.flatten())


def view_taskapp_page_sections(request):
    context = context_base()
    context['sections'] = TaskSection.objects.filter(published=True, ).order_by('id')

    return render(request, "taskapp/taskapp-page-sections.html", context.flatten())


def show_view_info_page(request, context, info_text):
    context = context_base()
    context['info_text'] = info_text

    return render(request, "taskapp/taskapp-info-page.html", context.flatten())


def view_task_solo(request, number):
    context = context_base()

    context['subtitle'] = str(Task.objects.get(number=number).section.name) + ': вопрос №' + str(number)
    template = ''

    template, context = task(request, template, context, number)
    context['task_wrap'] = 'taskapp/taskapp-task-only.html'
    request.session['task']['solo'] = 'GOOOD-SOLO'

    return render(request, template, context.flatten())


def view_section(request, sectionid):
    context = context_base()
    template = ''
    context['task_next_button'] = 'Попробовать другой вопрос'
    context['task_next_button_blue'] = 0
    sectionnow = TaskSection.objects.get(pk=sectionid)

    if TaskSection.objects.filter(published=True, parent=sectionid).count():
        context['sections'] = TaskSection.objects.filter(published=True, parent=sectionid).order_by('id')
        context['subtitle'] = sectionnow.name
        template = 'taskapp/taskapp-list-sections.html'

    else:
        # show task
        if request.method == 'POST':
            number = request.POST['task_number']
            context['task_next_button_blue'] = 1
            context['task_next_button'] = "Следующий вопрос"

        else:
            max_num = Task.objects.filter(published=True, section=TaskSection.objects.get(pk=sectionid)).count()
            if max_num < 1:
                context['info_text'] = 'В этом разделе  пока нет вопросов!'
                template = "taskapp/taskapp-info-page.html"
                return render(request, template, context)

            rand = randint(0, max_num - 1)
            number = Task.objects.filter(published=True, section=TaskSection.objects.get(pk=sectionid))[rand].number
            listme = request.session['task']
            listme[number] = 1
            request.session['task'] = listme

        context['subtitle'] = str(Task.objects.get(number=number).section.name)
        template, context = task(request, template, context, number)
        context['task_wrap'] = 'taskapp/taskapp-task-random.html'
    return render(request, template, context.flatten())


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
    return render(request, "test/test.html", context.flatten())


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

    return render(request, "test/test.html", context.flatten())
