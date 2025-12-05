from django.conf.urls import  url
from taskapp import views
from django.views.generic import RedirectView

urlpatterns = [
    #url(r'^test/$', views.test, name='test'),
    url(r'^$', views.view_taskapp_main_page, name='taskapp_main_page'),
    #url(r'^admin/test-admin/$', admin.task_edit, name='task_edit'),
    url(r'^section/$', RedirectView.as_view(url='/'), name='section_redirect'),
    url(r'^sections/$', views.view_taskapp_page_sections, name='sections'),
    url(r'^section/(?P<sectionid>[0-9]*)/$', views.view_section, name='sectionid'),
    url(r'^task/(?P<number>[0-9\-]*)/$', views.view_task_solo, name='number'),
]
