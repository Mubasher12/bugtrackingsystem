from django import forms
from django.contrib.auth.models import User
from .models import Project, UserProfile 
from .models import Bug, Developer

class BugStatusForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['status']

class BugEditForm(forms.ModelForm):
    # Adjust the queryset to match your User model's role field or relationship
    assigned_developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(userprofile__role='Developer'),  # Assuming 'role' is in UserProfile
        widget=forms.CheckboxSelectMultiple,  # Use 'forms.SelectMultiple' for a dropdown
        required=False
    )

    class Meta:
        model = Bug
        fields = ['title', 'description', 'status', 'assigned_developers']

class BugForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=Developer.objects.all(), 
        widget=forms.SelectMultiple,  # Multi-select widget
        label='Assigned Developers'
    )
    class Meta:
        model = Bug
        fields = ['title', 'description', 'deadline', 'screenshot', 'type', 'status', 'assigned_to']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'screenshot': forms.FileInput(attrs={'multiple': False}),  # Allow only one file
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),  
        }


    def clean_screenshot(self):
        screenshot = self.cleaned_data.get('screenshot')
        if screenshot:
            ext = screenshot.name.split('.')[-1].lower()
            if ext not in ['png', 'gif']:
                raise forms.ValidationError("Only .png and .gif files are allowed.")
        return screenshot

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.USER_ROLES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user

class ProjectForm(forms.ModelForm):
    # #mubasher changed
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'assigned_users']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # #mubasher changed
        if self.instance and self.instance.pk:
            self.fields['assigned_users'].initial = self.instance.assigned_to.all()

    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
            self.save_m2m()
        return project
