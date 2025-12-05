from django.conf.urls import  url
from taskapp import views
from django.views.generic import RedirectView

urlpatterns = [
    #url(r'^test/$', views.test, name='test'),
    url(r'^$', views.view_taskapp_main_page, name='taskapp_main_page'),
    url(r'^section/$', RedirectView.as_view(url='/'), name='section_redirect'),
    url(r'^section/(?P<section>[A-Za-z0-9\-]*)/$', views.view_task_solo_random, name='section'),
    url(r'^task/(?P<number>[0-9\-]*)/$', views.view_task_solo, name='number'),
]
