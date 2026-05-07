from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

ACCOUNT_STATUS_CHOICES = [
    (0 , "applicant"),
    (1 , "employer")
]

class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    status = models.BooleanField(choices=ACCOUNT_STATUS_CHOICES , default=0)
    email_verified = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

STATUS_CHOICES = [
    ('applied', 'Applied'),
    ('reviewed', 'Reviewed'),
    ('rejected', 'Rejected'),
    ('hired', 'Hired'),
]

def user_cv_path(instance , filename):
    user_id = instance.applicant.id if instance.applicant else "unknown"
    return f"cvs/user_{user_id}/job_{instance.job.id}/{filename}"

class Application(models.Model):
    job = models.ForeignKey(Job , on_delete=models.CASCADE)
    applicant = models.ForeignKey(User , on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    cv_file = models.FileField(upload_to=user_cv_path)
    status = models.CharField(choices=STATUS_CHOICES , default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    relevancy_score = models.FloatField(blank=True , null=True)

    class Meta:
        constraints = [   
            models.UniqueConstraint(
                fields=["job", "applicant"],
                name="unique_application_per_user_per_job"
            )
        ]
    

