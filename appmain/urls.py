from django.conf.urls import url

from . import views

app_name = 'appmain'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^plan/$', views.plan, name='plan'),
    url(r'^add_new_mail/$', views.add_new_mail, name='add_new_mail'),
    url(r'^sent_mail/$', views.sent_mail, name='sent_mail'),
]
