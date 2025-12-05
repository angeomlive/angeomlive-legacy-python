# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=250, unique=True,)

    def __str__(self):
        return self.name


class TaskSection(models.Model):
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=250, unique=True,)
    image = models.ImageField(upload_to='task/images/', verbose_name='image-section', null=True, blank=True)
    published = models.BooleanField(default=True,)

    def __str__(self):
        return self.name


class Task(models.Model):
    number = models.IntegerField(primary_key=True)
    section = models.ForeignKey('TaskSection',  related_name='task_section', null=True, blank=True)
    type = models.ForeignKey('TaskType', related_name='task_type', null=True, blank=True)
    published = models.BooleanField(default=True)
    id_inclass = models.IntegerField(default=0)
	

    def edit_task(self):
        return '<a href="/admin/task-edit/?task='+str(self.number)+'">Edit</a>'

    def number_show(self):
        return '<a href="/admin/task-edit/?task='+str(self.number)+'">'+str(self.number)+'</a>'

    def link_to_show_task(self):
        return '<a href="/task/'+str(self.number)+'/">Look</a>'

    def task_text(self):
        if self.type.id == 1:
            return unicode(TaskType1.objects.get(pk=self.id_inclass).text)
        elif self.type.id == 2:
            return unicode(TaskType2.objects.get(pk=self.id_inclass).text)
        else:
            return str(self.number)

    edit_task.allow_tags = True
    number_show.allow_tags = True
    task_text.allow_tags = True
    link_to_show_task.allow_tags = True
	
	

class TaskType1(models.Model):
    text = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    image = models.ImageField(upload_to='task/images/', verbose_name='image-type1', null=True, blank=True)

    def __str__(self):
        return self.text


class TaskType2(models.Model):
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='task/images/', verbose_name='image-type2', null=True, blank=True)
    variant_true = models.ForeignKey('TaskType2Variant', verbose_name='variant-true', null=True, blank=True)

    def __str__(self):
        return self.text


class TaskType2Variant(models.Model):
    text = models.CharField(max_length=500, verbose_name='task2')
    task = models.ForeignKey('TaskType2', verbose_name='task2-task', null=True, blank=True)

    def __str__(self):
        return self.text
