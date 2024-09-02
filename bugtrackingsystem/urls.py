from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views
from .views import qa_edit_project

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/signup/', permanent=True)),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('qa-dashboard/', views.qa_dashboard, name='qa_dashboard'),
    path('developer/landing/', views.developer_landing, name='developer_landing'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/', views.manager_dashboard, name='project_list'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('assigned-projects/', views.assigned_projects, name='assigned_projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
 
    path('projects/<int:project_id>/edit/', views.qa_edit_project, name='qa_edit_project'),

]

