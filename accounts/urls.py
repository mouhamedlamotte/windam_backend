from django.urls import path

from .views import ListUserAccountView, RetrieveUpdateDestroyAccountView, AddUserAccountView

urlpatterns = [
    path("", ListUserAccountView.as_view(), name="users_list"),
    path("<int:pk>/", RetrieveUpdateDestroyAccountView.as_view(), name="users_retrive_destroy"),
    path("add/", AddUserAccountView.as_view(), name="users_add"),
]
    