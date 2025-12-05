# -*- coding: utf-8 -*-

from django.contrib import admin
from django.shortcuts import render, redirect
from django.template import Context
from random import randint
from .models import TaskType, TaskSection, Task, TaskType1, TaskType2, TaskType2Variant

from adminplus.sites import AdminSitePlus
admin.site = AdminSitePlus()

class TaskAdmin(admin.ModelAdmin):
    pass
    list_display = ('number_show', 'edit_task', 'task_text', 'section', 'type', 'published', 'link_to_show_task',)


class TaskSectionAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'id', 'slug', 'published')
    prepopulated_fields = {"slug": ("name",)}


class TaskTypeAdmin(admin.ModelAdmin):
    pass
    list_display = ('name', 'id', 'slug')
    prepopulated_fields = {"slug": ("name",)}


class TaskType1Admin(admin.ModelAdmin):
    pass
    list_display = ('id', 'text', 'answer')


class TaskType2Admin(admin.ModelAdmin):
    pass


class TaskType2VariantAdmin(admin.ModelAdmin):
    pass


admin.site.register(TaskType1, TaskType1Admin)
admin.site.register(TaskType2, TaskType2Admin)
admin.site.register(TaskType2Variant, TaskType2VariantAdmin)
admin.site.register(TaskType, TaskTypeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskSection, TaskSectionAdmin)


def context_base_admin():
    return Context({
        'title': 'Редактирование вопроса: ',
    })


def task_edit_pre(context, number):
    template = ''
    task_option = Task.objects.get(number=number)
    context['title'] = context['title'] + ' ' + str(number)
    context['task_option'] = task_option
    context['sections'] = TaskSection.objects.all()

    if task_option.type.id == 1:
        context['task'] = TaskType1.objects.get(pk=task_option.id_inclass)
        template = 'admin/task-edit-type1.html'

    elif task_option.type.id == 2:
        context['task'] = TaskType2.objects.get(pk=task_option.id_inclass)
        template = 'admin/task-edit-type2.html'
        context['variants'] = TaskType2Variant.objects.filter(task=TaskType2.objects.get(pk=task_option.id_inclass))
        context['list'] = list(
            range(8 - TaskType2Variant.objects.filter(task=TaskType2.objects.get(pk=task_option.id_inclass)).count())
        )
    else:
        print('No types')

    return template, context


def task_edit_details(request, number):
    task_option = Task.objects.get(number=number)
    task_option.section = TaskSection.objects.get(pk=int(request.POST.get('section')))

    if str(request.POST.get('published')) == 'on':
        task_option.published = True
    else:
        task_option.published = False

    task_option.save()

    if task_option.type.id == 1:
        task = TaskType1.objects.get(pk=task_option.id_inclass)

        task.text = request.POST.get('text')
        task.answer = request.POST.get('answer')
        if request.FILES.get('image'):
            task.image = request.FILES.get('image')
            task.image.name = 'task-' + str(task_option.number) + '.jpg'
        task.save()

    elif task_option.type.id == 2:
        task = TaskType2.objects.get(pk=task_option.id_inclass)

        task.text = request.POST.get('text')
        if request.FILES.get('image'):
            task.image = request.FILES.get('image')
            task.image.name = 'task-' + str(task_option.number) + '.jpg'

        for variant in TaskType2Variant.objects.filter(task=TaskType2.objects.get(pk=task_option.id_inclass)):
            if request.POST['variant-' + str(variant.id)]:
                variant.text = request.POST['variant-' + str(variant.id)]
                variant.save()
                if str(variant.id) == request.POST['variant-true']:
                    task.variant_true = variant

        for i in range(8 - TaskType2Variant.objects.filter(
                task=TaskType2.objects.get(pk=task_option.id_inclass)).count()):
            if request.POST['variant-' + str(i)]:
                variant = TaskType2Variant()
                variant.text = request.POST['variant-' + str(i)]
                variant.task = task
                variant.save()
                if str(i) == request.POST['variant-true']:
                    task.variant_true = variant
                    task.save()


@admin.site.register_view('task-edit/', 'Edit task')
def task_edit(request):
    pass
    context = context_base_admin()
    template = ''

    number = int(request.GET.get('task'))
    if request.method == 'GET':
        template, context = task_edit_pre(context, number)

    elif request.method == 'POST':
        task_edit_details(request, number)
        template = 'admin/task-edit-ok.html'
        task_option = Task.objects.get(number=number)
        context['title'] = 'Вопрос №' + str(task_option.number) + ' успешно отредактирован!'
        context['task_option'] = task_option

    return render(request, template, context)


@admin.site.register_view('add-task/', 'Добавить новый вопрос')
def task_add(request):
    pass
    context = context_base_admin()
    template = ''

    if request.method == 'POST':
        task_option = Task()
        task_option.type = TaskType.objects.get(pk=int(request.POST['type']))

        number = randint(1000, 9999)
        while Task.objects.filter(number=number).count():
            number = randint(1000, 9999)
        task_option.number = number

        if task_option.type.id == 1:
            task = TaskType1()
            task.save()
            task_option.id_inclass = task.id

        elif task_option.type.id == 2:
            task = TaskType2()
            task.save()
            task_option.id_inclass = task.id

        task_option.save()

        return redirect('/admin/task-edit/?task='+str(number))
    else:
        template = 'admin/task-add.html'
        context['title'] = 'Выберете тип вопроса, который вы хотите создать: '
        context['types'] = TaskType.objects.all()

    return render(request, template, context)


