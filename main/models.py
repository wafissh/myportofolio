import uuid
from django.db import models
from django.utils import timezone

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('organization', "Organization experience")
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class TechStack(models.Model):
    class Category(models.TextChoices):
         
        BACKEND = 'BACKEND', 'Backend Framework'          # Django, FastAPI, Express, Laravel
        DATABASE = 'DATABASE', 'Database'                  # PostgreSQL, MySQL, MongoDB, Redis
        API = 'API', 'API & Integration'                   
        
        FRONTEND = 'FRONTEND', 'Frontend Web'               
        
        CLOUD = 'CLOUD', 'Cloud & Hosting'                  
        DEVOPS = 'DEVOPS', 'DevOps & CI/CD'                 
        AI_ML = 'AI_ML', 'AI / Machine Learning'            # TensorFlow, OpenCV, LangChain
        LANGUAGE = 'LANGUAGE', 'Programming Language'
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=20, 
        choices=Category.choices, 
        default=Category.BACKEND
    )
    icon_class = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Class icon, misal: 'devicon-python-plain' atau SVG path"
    )
    

    class Meta:
        verbose_name_plural = "Tech Stacks"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    role = models.CharField(max_length=150, blank=True, help_text="Contoh: Frontend Developer & Deployment Specialist")
    description = models.TextField()
    thumbnail = models.URLField()
    project_url = models.URLField(blank=True, null=True, help_text="Link ke live site atau GitHub")
    is_featured = models.BooleanField(default=False)
    
    # Relasi Many-to-Many ke TechStack
    tech_stacks = models.ManyToManyField(
        TechStack, 
        related_name='projects',
        blank=True
    )

    def __str__(self):
        return self.title
    
class Education(models.Model):
    title = models.CharField(max_length=255)
    started_at = models.DateTimeField(default=timezone.now, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    education_loc = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    