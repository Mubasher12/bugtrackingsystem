from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    USER_ROLES = (
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('QA', 'QA'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=USER_ROLES)

     
    def __str__(self):
        return self.user.username
    def is_qa(self):
        return self.role == 'QA'

    def is_manager(self):
        return self.role == 'Manager'
     

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=datetime.date(2024, 12, 31))
    manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    assigned_to = models.ManyToManyField(UserProfile, blank=True, related_name='assigned_projects')
    developers = models.ManyToManyField(User, related_name='projects_as_developer', blank=True)  # Ensure this field is correctly defined
    qa_members = models.ManyToManyField(User, related_name='projects_as_qa', blank=True)

    # developers = models.ManyToManyField(UserProfile, related_name='projects')
    assigned_developers = models.ManyToManyField(UserProfile, related_name='projects', limit_choices_to={'role': 'Developer'})
    assigned_qas = models.ManyToManyField(UserProfile, related_name='qa_projects', limit_choices_to={'role': 'QA'})

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255, default='Default Title')
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
# class Developer(models.Model):  #mubasher changed
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  #mubasher changed
#     # Add any additional fields you need  #mubasher changed

#     def __str__(self):  #mubasher changed
#         return self.user.username  #mubasher changed
# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone
# import datetime
# class UserProfile(models.Model):
#     USER_ROLES = (
#         ('Manager', 'Manager'),
#         ('Developer', 'Developer'),
#         ('QA', 'QA'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=USER_ROLES)

#     def __str__(self):
#         return self.user.username

#     def is_manager(self):
#         return self.role == 'Manager'

#     # def is_qa(self):
#     #     return self.role == 'QA'

# class Project(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     start_date = models.DateField(default=timezone.now)
#     end_date = models.DateField(default=datetime.date(2024, 12, 31))
#     # end_date = models.DateField(default=timezone.now)
#     manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
#     assigned_to = models.ManyToManyField(UserProfile, blank=True, related_name='assigned_projects')

#     def __str__(self):
#         return self.name

# class Task(models.Model):
#     title = models.CharField(max_length=255, default='Default Title')
#     description = models.TextField()
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateField(default=timezone.now)

#     def __str__(self):
#         return self.title
    
#mubasherchangedfrom here

# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# class UserProfile(models.Model):
#     USER_ROLES = (
#         ('Manager', 'Manager'),
#         ('Developer', 'Developer'),
#         ('QA', 'QA'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=USER_ROLES)

#     def __str__(self):
#         return self.user.username

#     def is_manager(self):
#         return self.role == 'Manager'

#     def is_qa(self):
#         return self.role == 'QA'

# class Project(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
#     assigned_to = models.ManyToManyField(UserProfile, blank=True, related_name='assigned_projects')

#     def __str__(self):
#         return self.name

# class Task(models.Model):
#     title = models.CharField(max_length=255, default='Default Title')  # Default title added
#     description = models.TextField()
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateField(default=timezone.now)  # Use timezone.now as a callable

#     def __str__(self):
#         return self.title
