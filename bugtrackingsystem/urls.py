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
    path('landing-page/', views.landing_page, name='landing_page'),
    # path('create_bug/', views.create_bug, name='create_bug'),
    path('create_bug/', views.create_bug, name='create_bug'),
    path('bugs/', views.bug_list, name='bug_list'),
    path('developer/assigned-bugs/', views.developer_assigned_bugs, name='developer_assigned_bugs'),
    path('bugs/edit/<int:id>/', views.edit_bug, name='edit_bug'),  # Add this line
    path('developer/bugs/update/<int:bug_id>/', views.update_bug_status, name='update_bug_status'),
    path('projects/<int:project_id>/bugs/', views.view_bugs, name='view_bugs'),




 
    path('projects/<int:project_id>/edit/', views.qa_edit_project, name='qa_edit_project'),

]

