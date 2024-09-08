from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Project, Assignment
from .forms import SignupForm, ProjectForm
# from .forms import EditProjectQAForm 
from django.forms import modelformset_factory
  # Create this form for handling developer assignments



def qa_edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Get all developers currently assigned to the project
    assigned_developers = Assignment.objects.filter(project=project, user__userprofile__role='Developer')
    
    # Get all developers not currently assigned to the project
    all_developers = User.objects.filter(userprofile__role='Developer')
    available_developers = all_developers.exclude(id__in=assigned_developers.values_list('user_id', flat=True))
    
    if request.method == 'POST':
        # Handle removing developers
        if 'remove_developer' in request.POST:
            developer_id = request.POST.get('remove_developer')
            Assignment.objects.filter(project=project, user_id=developer_id).delete()
        
        # Handle adding developers
        if 'add_developers' in request.POST:
            developer_ids = request.POST.getlist('add_developers')  # Get list of selected developers
            for developer_id in developer_ids:
                developer = get_object_or_404(User, id=developer_id)
                Assignment.objects.get_or_create(project=project, user=developer)
        
        return redirect('qa_edit_project', project_id=project.id)
    
    context = {
        'project': project,
        'assigned_developers': assigned_developers,
        'available_developers': available_developers,
    }
    
    return render(request, 'qa_edit_project.html', context)



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

@login_required
@login_required
def qa_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'qa_landing.html', {'projects': projects})



@login_required
@login_required
def developer_landing(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'developer_landing.html', {'projects': projects})




@login_required
@login_required
def assigned_projects(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    projects = Project.objects.filter(assigned_to=user_profile)
    return render(request, 'assigned_projects.html', {'projects': projects})


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

