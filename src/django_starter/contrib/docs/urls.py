from django.urls import path

from . import views

app_name = "djs_docs"

urlpatterns = [
    path("", views.docs_index, name="index"),
    path("<slug:slug>/", views.docs_detail, name="detail"),
]
