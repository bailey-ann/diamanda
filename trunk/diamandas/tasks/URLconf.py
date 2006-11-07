from django.conf.urls.defaults import *

# Wiki* URLs
urlpatterns = patterns('tasks',
(r'^task_show/(?P<task_id>(\d+))/$', 'views.task_show'),
(r'^task_add/$', 'views.task_add'),
(r'^task_list/(?P<pagination_id>(\d+))/$', 'views.task_list'),
(r'^task_com_add/(?P<task_id>(\d+))/$', 'views.com_task_add'),
)
