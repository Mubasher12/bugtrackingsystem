from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Project 
from .forms import SignupForm, ProjectForm
# from .forms import EditProjectQAForm 
from django.forms import modelformset_factory
  # Create this form for handling developer assignments

def remove_developer(request, project_id, developer_id):
    project = get_object_or_404(Project, id=project_id)
    developer = get_object_or_404(UserProfile, id=developer_id)
    
    if developer in project.developers.all():
        project.developers.remove(developer)
    
    return redirect('edit_project_qa', project_id=project_id)


@login_required
def edit_project_qa(request, project_id):
    # Fetch the project by ID
    project = get_object_or_404(Project, id=project_id)
    
    # Get all developers assigned to this project
    assigned_developers = project.developers.all()
    
    # Get all available developers
    all_developers = UserProfile.objects.all()
    
    # Pass data to the template
    return render(request, 'edit_project_qa.html', {
        'project': project,
        'assigned_developers': assigned_developers,
        'all_developers': all_developers,
    })
def add_developer(request, project_id):
    if request.method == 'POST':
        # Get the developer ID from the POST data
        developer_id = request.POST.get('developer_id')
        
        # Fetch the developer and project objects
        developer = get_object_or_404(UserProfile, id=developer_id)
        project = get_object_or_404(Project, id=project_id)
        
        # Add the developer to the project if they're not already assigned
        if developer not in project.developers.all():
            project.developers.add(developer)
        
    # Redirect back to the edit page
    return redirect('edit_project_qa', project_id=project_id)
# def edit_project_qa(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     available_developers = UserProfile.objects.exclude(id__in=project.developers.all())

#     if request.method == 'POST':
#         if 'add_developer' in request.POST:
#             developer_id = request.POST.get('developer')
#             if developer_id:
#                 developer = get_object_or_404(UserProfile, id=developer_id)
#                 project.developers.add(developer)
#                 project.save()
#                 # Redirect to the same page after adding a developer
#                 return redirect('edit_project_qa', project_id=project.id)

#         elif 'remove_developer' in request.POST:
#             developer_id = request.POST.get('developer_id')
#             if developer_id:
#                 developer = get_object_or_404(UserProfile, id=developer_id)
#                 project.developers.remove(developer)
#                 project.save()
#                 # Redirect to the same page after removing a developer
#                 return redirect('edit_project_qa', project_id=project.id)

#     return render(request, 'edit_project_qa.html', {
#         'project': project,
#         'available_developers': available_developers,
#     }) agr km na bna to isko revert kr dnga
# def edit_project_qa(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
    
#     if request.method == 'POST':
#         form = EditProjectQAForm(request.POST, project=project)
#         if form.is_valid():
#             # Update the project's developers
#             updated_developers = form.cleaned_data['developers']
#             project.developers.set(updated_developers)
#             return redirect('qa_dashboard')  # Redirect to QA dashboard
#     else:
#         form = EditProjectQAForm(project=project)
#     form.fields['developers'].initial = project.developers.all()
    # Pass the assigned developers to the template km bn gya to thek vrna isa change kr lnga
    # assigned_developers = project.developers.all() assigned_developers': assigned_developers
    
    # return render(request, 'edit_project_qa.html', {'form': form, 'project': project,})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            
            if user_profile.role == 'Manager':
                return redirect('manager_dashboard')
            elif user_profile.role == 'QA':
                return redirect('qa_dashboard')
            elif user_profile.role == 'Developer':
                return redirect('developer_landing')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project successfully deleted.')
        return redirect('manager_dashboard')
    
    return render(request, 'confirm_delete.html', {'project': project})

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def manager_dashboard(request):
    projects = Project.objects.all()
    return render(request, 'manager_dashboard.html', {'projects': projects})

@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = UserProfile.objects.get(user=request.user)
            project.save()
            messages.success(request, "Project successfully created.")
            return redirect('manager_dashboard')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.userprofile.is_manager():
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                project = form.save(commit=False)
                assigned_users = request.POST.getlist('assigned_to')  # Get the list of assigned users
                project.assigned_to.set(UserProfile.objects.filter(id__in=assigned_users))
                # project.assigned_to.set(assigned_users)  # Assign the selected users to the project
                project.save()
                messages.success(request, "Project updated successfully.")
                return redirect('manager_dashboard')
        else:
            form = ProjectForm(instance=project)
        users = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')
        selected_users = project.assigned_to.values_list('id', flat=True) 
        return render(request, 'edit_project.html', {'form': form, 'users': users, 'selected_users': selected_users})
    else:
        return redirect('unauthorized')  # Redirect if a non-manager tries to access the edit page
# def edit_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.user.userprofile.is_manager():
#         # Manager can edit all fields
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 form.save()
#                 return redirect('project_detail', pk=pk)
#         else:
#             form = ProjectForm(instance=project)
#         # #mubasher changed
#         users = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')
#         selected_users = project.assigned_to.all()
#         return render(request, 'edit_project.html', {'form': form, 'users': users, 'selected_users': selected_users})
#     else:
#         # Handle permissions for non-Managers
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 # Allow only certain fields to be edited
#                 project.name = form.cleaned_data['name']
#                 project.description = form.cleaned_data['description']
#                 project.save()
#                 return redirect('project_detail', pk=pk)
#         else:
#             form = ProjectForm(instance=project)
    
#     return render(request, 'edit_project.html', {'form': form})

@login_required
@login_required
def qa_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'qa_landing.html', {'projects': projects})

# def qa_dashboard(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'qa_landing.html', {'projects': projects})

@login_required
@login_required
def developer_landing(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'developer_landing.html', {'projects': projects})


# def developer_landing(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'developer_landing.html', {'projects': projects})

@login_required
@login_required
def assigned_projects(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'assigned_projects.html', {'projects': projects})

# def assigned_projects(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'assigned_projects.html', {'projects': projects})

@login_required
def assign_project(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)
    project.assigned_to.add(user)
    project.save()
    return redirect('manager_dashboard')

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def user_projects(request):
    user_projects = request.user.projects.all()
    return render(request, 'user_projects.html', {'projects': user_projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login as auth_login
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .models import UserProfile, Project, Task
# from .forms import SignupForm, ProjectForm

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Signup successful. Please log in.")
#             return redirect('login')
#     else:
#         form = SignupForm()
    
#     return render(request, 'signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             user_profile = UserProfile.objects.get(user=user)
            
#             if user_profile.role == 'Manager':
#                 return redirect('manager_dashboard')
#             elif user_profile.role == 'QA':
#                 return redirect('qa_dashboard')
#             elif user_profile.role == 'Developer':
#                 return redirect('developer_landing')
#         else:
#             messages.error(request, 'Invalid username or password')
    
#     return render(request, 'login.html')

# @login_required
# def delete_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
    
#     if request.method == 'POST':
#         project.delete()
#         messages.success(request, 'Project successfully deleted.')
#         return redirect('manager_dashboard')
    
#     return render(request, 'confirm_delete.html', {'project': project})

# @login_required
# def home(request):
#     return render(request, 'home.html')

# @login_required
# def manager_dashboard(request):
#     projects = Project.objects.all()
#     return render(request, 'manager_dashboard.html', {'projects': projects})

# @login_required
# def create_project_view(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.manager = UserProfile.objects.get(user=request.user)
#             project.save()
#             messages.success(request, "Project successfully created.")
#             return redirect('manager_dashboard')
#     else:
#         form = ProjectForm()

#     return render(request, 'create_project.html', {'form': form})

# @login_required
# def edit_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.user.userprofile.is_manager():
#         # Manager can edit all fields
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 form.save()
#                 return redirect('project_detail', pk=pk)
#         else:
#             form = ProjectForm(instance=project)
#         # #mubasher changed
#         users = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')
#         selected_users = project.assigned_to.all()
#         return render(request, 'edit_project.html', {'form': form, 'users': users, 'selected_users': selected_users})
#     else:
#         # Handle permissions for non-Managers
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 # Allow only certain fields to be edited
#                 project.name = form.cleaned_data['name']
#                 project.description = form.cleaned_data['description']
#                 project.save()
#                 return redirect('project_detail', pk=pk)
#         else:
#             form = ProjectForm(instance=project)
    
#     return render(request, 'edit_project.html', {'form': form})

# @login_required
# def qa_dashboard(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'qa_landing.html', {'projects': projects})

# @login_required
# def developer_landing(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'developer_landing.html', {'projects': projects})

# @login_required
# def assigned_projects(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'assigned_projects.html', {'projects': projects})

# @login_required
# def assign_project(request, project_id, user_id):
#     project = get_object_or_404(Project, id=project_id)
#     user = get_object_or_404(User, id=user_id)
#     project.assigned_to.add(user)
#     project.save()
#     return redirect('manager_dashboard')

# @login_required
# def project_list(request):
#     projects = Project.objects.all()
#     return render(request, 'project_list.html', {'projects': projects})

# @login_required
# def user_projects(request):
#     user_projects = request.user.projects.all()
#     return render(request, 'user_projects.html', {'projects': user_projects})

# def project_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     return render(request, 'project_detail.html', {'project': project})


# def edit_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if user_profile.is_manager():
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 form.save()
#                 return redirect('manager_dashboard')
#         else:
#             form = ProjectForm(instance=project)

#     elif user_profile.is_qa():
#         if request.method == 'POST':
#             assigned_users = request.POST.getlist('assigned_to')
#             project.assigned_to.set(UserProfile.objects.filter(id__in=assigned_users))
#             return redirect('qa_landing')
#         else:
#             form = ProjectForm(instance=project)
#             form.fields['name'].disabled = True
#             form.fields['description'].disabled = True
#             form.fields['manager'].disabled = True

#     else:
#         return redirect('no_permission')

#     return render(request, 'edit_project.html', {'form': form, 'project': project})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login as auth_login
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required,user_passes_test
# from .models import UserProfile, Project, Task
# from .forms import SignupForm, ProjectForm

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Signup successful. Please log in.")
#             return redirect('login')  # Redirect to login page
#     else:
#         form = SignupForm()
    
#     return render(request, 'signup.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             user_profile = UserProfile.objects.get(user=user)
            
#             if user_profile.role == 'Manager':
#                 return redirect('manager_dashboard')
#             elif user_profile.role == 'QA':
#                 return redirect('qa_landing')
#             elif user_profile.role == 'Developer':
#                 return redirect('developer_landing')
#         else:
#             messages.error(request, 'Invalid username or password')
    
#     return render(request, 'login.html')

# @login_required
# def delete_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
    
#     if request.method == 'POST':
#         project.delete()
#         messages.success(request, 'Project successfully deleted.')
#         return redirect('manager_dashboard')  # Redirect to the manager dashboard after deletion
    
#     return render(request, 'confirm_delete.html', {'project': project})

# @login_required
# def home(request):
#     return render(request, 'home.html')

# @login_required
# def manager_dashboard(request):
#     projects = Project.objects.all()
#     return render(request, 'manager_dashboard.html', {'projects': projects})

# @login_required
# def create_project_view(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.manager = UserProfile.objects.get(user=request.user)  # Ensure manager is assigned
#             project.save()
#             messages.success(request, "Project successfully created.")
#             return redirect('manager_dashboard')
#     else:
#         form = ProjectForm()

#     return render(request, 'create_project.html', {'form': form})

# @login_required
# def edit_project(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     user_profile = UserProfile.objects.get(user=request.user)

#     if user_profile.is_manager():
#         # Managers can edit all details of the project
#         if request.method == 'POST':
#             form = ProjectForm(request.POST, instance=project)
#             if form.is_valid():
#                 form.save()
#                 return redirect('manager_dashboard')
#         else:
#             form = ProjectForm(instance=project)

#     elif user_profile.is_qa():
#         # QA can only add or remove developers from the project
#         if request.method == 'POST':
#             assigned_users = request.POST.getlist('assigned_to')
#             project.assigned_to.set(UserProfile.objects.filter(id__in=assigned_users))
#             return redirect('qa_dashboard')
#         else:
#             form = ProjectForm(instance=project)
#             # Restrict the fields that QA can edit
#             form.fields['name'].disabled = True
#             form.fields['description'].disabled = True
#             form.fields['manager'].disabled = True

#     else:
#         # If the user doesn't have permission, redirect or show an error
#         return redirect('no_permission')

#     return render(request, 'edit_project.html', {'form': form, 'project': project})

# @login_required
# # def edit_project(request, pk):
# #     project = get_object_or_404(Project, pk=pk)

# #     if request.method == 'POST':
# #         form = ProjectForm(request.POST, instance=project)
# #         if form.is_valid():
# #             project = form.save(commit=False)
            
# #             # Handle selected users from multi-select dropdown
# #             selected_user_ids = request.POST.getlist('assigned_to')
# #             selected_users = UserProfile.objects.filter(id__in=selected_user_ids)
            
# #             # Update project with selected users
# #             project.assigned_to.set(selected_users)  # Assuming `assigned_to` is ManyToManyField
            
# #             project.save()
# #             messages.success(request, "Project successfully updated.")
# #             return redirect('manager_dashboard')
# #     else:
# #         form = ProjectForm(instance=project)
    
# #     # Get all users, first developers then QA
# #     developers = UserProfile.objects.filter(role='Developer')
# #     qa_users = UserProfile.objects.filter(role='QA')
# #     users = list(developers) + list(qa_users)

# #     # Get selected user IDs for pre-selection in the dropdown
# #     selected_users = project.assigned_to.values_list('id', flat=True)

# #     return render(request, 'edit_project.html', {
# #         'form': form,
# #         'users': users,
# #         'selected_users': selected_users
# #     })
# def qa_landing(request):
#     # Fetch the UserProfile associated with the current user
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     # Fetch projects assigned to this UserProfile
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'qa_landing.html', {'projects': projects})
# # def qa_landing(request):
# #     projects = Project.objects.filter(assigned_to=request.user)  # Fetch assigned projects
# #     tasks = Task.objects.filter(assigned_to=request.user)
# #     return render(request, 'qa_landing.html', {'tasks': tasks, 'projects': projects})

# @login_required
# def developer_landing(request):
#     # Fetch the UserProfile associated with the current user
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     # Fetch projects assigned to this UserProfile
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'developer_landing.html', {'projects': projects})
# # def developer_landing(request):
# #     projects = Project.objects.filter(assigned_to=request.user)  # Fetch assigned projects
# #     tasks = Task.objects.filter(assigned_to=request.user)
# #     return render(request, 'developer_landing.html', {'tasks': tasks, 'projects': projects})

# # @login_required
# # def qa_landing(request):
# #     tasks = Task.objects.filter(assigned_to=request.user)
# #     return render(request, 'qa_landing.html', {'tasks': tasks})

# # @login_required
# # def developer_landing(request):
# #     tasks = Task.objects.filter(assigned_to=request.user)
# #     return render(request, 'developer_landing.html', {'tasks': tasks})

# @login_required
# def assigned_projects(request):
#     user_profile = UserProfile.objects.get(user=request.user)
#     projects = Project.objects.filter(assigned_to=user_profile)
#     return render(request, 'assigned_projects.html', {'projects': projects})

# @login_required
# def assign_project(request, project_id, user_id):
#     project = get_object_or_404(Project, id=project_id)
#     user = get_object_or_404(User, id=user_id)
#     project.assigned_to.add(user)  # Add user to the project's assigned_to
#     project.save()
#     return redirect('manager_dashboard')

# @login_required
# def project_list(request):
#     projects = Project.objects.all()
#     return render(request, 'project_list.html', {'projects': projects})

# @login_required
# def user_projects(request):
#     user_projects = request.user.projects.all()
#     return render(request, 'user_projects.html', {'projects': user_projects})
# def project_detail(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     return render(request, 'project_detail.html', {'project': project})