from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'token_view$', views.token_view)

]