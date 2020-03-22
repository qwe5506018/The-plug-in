


from django.conf.urls import url
from . import views

urlpatterns = [
    #127.0.0.1:8000/user/user
    url(r"^index$",views.user_get),
    url(r"^verify$",views.verify_user),
    url(r"^login$",views.user_data),
    url(r"^modify$",views.modify_user),

]