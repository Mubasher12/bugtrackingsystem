from django import forms
from django.contrib.auth.models import User
from .models import Project, UserProfile 

# class EditProjectQAForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'start_date', 'end_date', 'developers'] 

#         developers = forms.ModelMultipleChoiceField(
#         queryset=User.objects.filter(role='Developer'),
#         widget=forms.CheckboxSelectMultiple
#     )
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
# class EditProjectQAForm(forms.ModelForm):
#     developers = forms.ModelMultipleChoiceField(
#         queryset=User.objects.filter(groups__name='Developer'),  # Filter developers if needed
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
    
#     class Meta:
#         model = Project
#         fields = ['developers']  # Only include the developers field
# from 
# django import forms
# from django.contrib.auth.models import User
# from .models import Project, UserProfile

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     role = forms.ChoiceField(choices=UserProfile.USER_ROLES, widget=forms.RadioSelect)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
#         return user

# class ProjectForm(forms.ModelForm):
#     # #mubasher changed
#     assigned_users = forms.ModelMultipleChoiceField(
#         queryset=UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username'),
#         widget=forms.SelectMultiple,
#         required=False
#     )

#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'start_date', 'end_date', 'assigned_users']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # #mubasher changed
#         if self.instance and self.instance.pk:
#             self.fields['assigned_users'].initial = self.instance.assigned_to.all()

#     def save(self, commit=True):
#         project = super().save(commit=False)
#         if commit:
#             project.save()
#             self.save_m2m()
#         return project
#mubasherchanged from here. 

# from django import forms
# from django.contrib.auth.models import User
# from .models import Project, UserProfile

# class SignupForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             # Create a UserProfile for the new user if necessary
#             UserProfile.objects.create(user=user)
#         return user

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'assigned_to']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()
#         self.fields['assigned_to'].queryset = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')

#     def save(self, commit=True):
#         project = super().save(commit=False)
#         if commit:
#             project.save()
#             self.save_m2m()
#         return project

# # from django import forms
# # from .models import Project, UserProfile

# # class SignupForm(forms.ModelForm):
# #     class Meta:
# #         model = UserProfile
# #         fields = ['username', 'email', 'password']  # Adjust fields as necessary
# # class ProjectForm(forms.ModelForm):
# #     class Meta:
# #         model = Project
# #         fields = ['name', 'description', 'assigned_to']

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()
# #         self.fields['assigned_to'].queryset = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')

# #     def save(self, commit=True):
# #         project = super().save(commit=False)
# #         if commit:
# #             project.save()
# #             self.save_m2m()
# #         return project

# from django import forms
# from django.contrib.auth.models import User
# from .models import Project, UserProfile, Task

# USER_TYPE_CHOICES = [
#     ('Developer', 'Developer'),
#     ('QA', 'QA'),
#     ('Manager', 'Manager'),
# ]

# class SignupForm(forms.ModelForm):
#     role = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             # Create and save a UserProfile with the selected role
#             user_profile = UserProfile(user=user, role=self.cleaned_data['role'])
#             user_profile.save()
#         return user

# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'assigned_to']  # Exclude start_date and end_date if not in the model

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Customizing the form fields if needed
#         self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()  # Use CheckboxSelectMultiple for many-to-many fields
#         self.fields['assigned_to'].queryset = UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username')

#     def save(self, commit=True):
#         project = super().save(commit=False)
#         if commit:
#             project.save()
#             self.save_m2m()  # Save many-to-many relationships
#         return project

# from django import forms
# from django.contrib.auth.models import User
# from .models import Project, UserProfile,Task

# USER_TYPE_CHOICES = [
#     ('Developer', 'Developer'),
#     ('QA', 'QA'),
#     ('Manager', 'Manager'),
# ]

# class SignupForm(forms.ModelForm):
#     role = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             # Create and save a UserProfile with the selected role
#             user_profile = UserProfile(user=user, role=self.cleaned_data['role'])
#             user_profile.save()
#         return user
# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description', 'start_date', 'end_date', 'assigned_to']  # Include the necessary fields

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Customizing the form fields if needed
#         self.fields['assigned_to'].widget.attrs.update({'class': 'form-control'})
#         self.fields['start_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
#         self.fields['end_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
# # class ProjectForm(forms.ModelForm):
# #     assigned_to = forms.ModelMultipleChoiceField(
# #         queryset=UserProfile.objects.filter(role__in=['Developer', 'QA']).order_by('role', 'user__username'),
# #         widget=forms.CheckboxSelectMultiple,
# #         required=False,
# #         label='Assign Users'
# #     )

# #     class Meta:
# #         model = Project
# #         fields = ['name', 'description', 'start_date', 'end_date', 'assigned_to']

#     def save(self, commit=True):
#         project = super().save(commit=False)
#         if commit:
#             project.save()
#             self.save_m2m()  # Save many-to-many relationships
#         return project
# class EditProjectQAForm(forms.ModelForm):
#     developers = forms.ModelMultipleChoiceField(
#         queryset=UserProfile.objects.filter(role='Developer'),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     class Meta:
#         model = Project
#         fields = ['developers']  # Only the developers field is editable

#     def __init__(self, *args, **kwargs):
#         project = kwargs.pop('project', None)
#         super().__init__(*args, **kwargs)
#         if project:
#             self.fields['developers'].initial = project.developers.all()