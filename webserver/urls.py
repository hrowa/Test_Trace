
from django.urls import path
from .views import SaveSceneDataView


urlpatterns = [
    path("save-data/", SaveSceneDataView.as_view(), name="save-data"),
]
