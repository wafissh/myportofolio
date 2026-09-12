from django.contrib import admin
from main.models import Experience, TechStack, Project, Education

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'started_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_class')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'role', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('title', 'description', 'role')
    list_editable = ('is_featured',)
    filter_horizontal = ('tech_stacks',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('title', 'education_loc', 'started_at')
    search_fields = ('title', 'education_loc')
