from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

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
    path('project/<int:project_id>/remove-developer/<int:developer_id>/', views.remove_developer, name='remove_developer'),
    # path('edit-project-qa/<int:project_id>/', views.edit_project_qa, name='edit_project_qa'),
    path('qa/project/edit/<int:project_id>/', views.edit_project_qa, name='edit_project_qa'),
    path('projects/<int:project_id>/edit/', views.edit_project_qa, name='edit_project_qa'),
    path('projects/<int:project_id>/add_developer/', views.add_developer, name='add_developer'),
    path('projects/<int:project_id>/remove_developer/<int:developer_id>/', views.remove_developer, name='remove_developer'),




]

# from django.contrib import admin
# from django.urls import path
# from django.views.generic import RedirectView
# from . import views

# urlpatterns = [
#     path('admin/', admin.site.urls),  # URL for the admin interface
#     path('', RedirectView.as_view(url='/signup/', permanent=True)),  # Redirect root URL to signup
#     path('signup/', views.signup_view, name='signup'),  # Signup page
#     path('login/', views.login_view, name='login'),  # Login page
#     path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
#     path('qa/landing/', views.qa_landing, name='qa_landing'),  # QA Landing page
#     path('developer/landing/', views.developer_landing, name='developer_landing'),  # Developer Landing page
#     path('create_project/', views.create_project_view, name='create_project'),  # Create project
#     path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),  # Edit project
#     path('projects/', views.manager_dashboard, name='project_list'),  # View all projects (Manager Dashboard)
#     path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),  # Delete project
#     path('assigned-projects/', views.assigned_projects, name='assigned_projects'),  # View assigned projects
#     path('projects/<int:pk>/', views.project_detail, name='project_detail'),  # Project detail
# ]
