from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, CheckboxInput, SelectMultiple
from django.utils.html import strip_tags
from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "role",
            "description",
            "thumbnail",
            "project_url",
            "is_featured",
            "tech_stacks",
        ]
        labels = {
            "title": "Nama Proyek",
            "slug": "Slug (URL-friendly name)",
            "role": "Role Kamu",
            "description": "Deskripsi Proyek",
            "thumbnail": "URL Gambar Thumbnail",
            "project_url": "URL Proyek",
            "is_featured": "Featured Project?",
            "tech_stacks": "Tech Stack",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 100,
                }
            ),
            "slug": TextInput(
                attrs={
                    "placeholder": "portfolio-website",
                }
            ),
            "role": TextInput(
                attrs={
                    "placeholder": "Fullstack Developer",
                    "maxlength": 150,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "is_featured": CheckboxInput(),
            "tech_stacks": SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["thumbnail"].required = False
        self.fields["project_url"].required = False

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_role(self):
        return strip_tags(self.cleaned_data["role"]).strip()

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi proyek tidak boleh hanya berisi tag HTML.")
        return description
