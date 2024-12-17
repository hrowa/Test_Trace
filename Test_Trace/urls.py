from django.contrib import admin
from django.urls import path, include
from webserver import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('webserver.urls')),
    path('scenes/<int:scene_id>/dashboard/', views.dashboard, name='dashboard'),
]
