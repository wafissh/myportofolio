import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
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
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class TechStack(models.Model):
    class Category(models.TextChoices):
        BACKEND = 'BACKEND', 'Backend & Database'
        FRONTEND = 'FRONTEND', 'Frontend & Mobile'
        DEVOPS = 'DEVOPS', 'DevOps & Tools'
        OTHER = 'OTHER', 'Other / Hardware / AI'
        
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
    description = models.TextField()
    thumbnail = models.URLField()
    
    # Relasi Many-to-Many ke TechStack
    tech_stacks = models.ManyToManyField(
        TechStack, 
        related_name='projects',
        blank=True
    )

    def __str__(self):
        return self.title