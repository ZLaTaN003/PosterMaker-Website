from . import views
from django.urls import path,include

urlpatterns = [
path("",views.makeposter,name="makeposter"),
]