



from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^interface$",views.interface),
    url(r"^antique$",views.antique),
    url(r"^information$",views.information),
    url(r"^today",views.today),
    url(r"^interface1$",views.Phount.as_view()),
    url(r"^search$",views.GoodsSearchView.as_view()),
]