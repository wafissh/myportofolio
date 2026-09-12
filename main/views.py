from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from collections import OrderedDict

from main.models import Experience, Project, TechStack, Education


def show_main(request):
    featured_project = Project.objects.filter(is_featured=True).first()
    featured_experiences = Experience.objects.filter(is_featured=True).order_by('-started_at')
    project_list = Project.objects.all()
    tech_stack = TechStack.objects.all()
    education_list = Education.objects.all().order_by('-started_at')
    experience_list = Experience.objects.all().order_by('started_at')[:4]
    exp_by_year = OrderedDict()
    for exp in experience_list:
        year = exp.started_at.year if exp.started_at else timezone.now().year
        exp_by_year.setdefault(year, []).append(exp)
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "npm": "2506624461",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "featured_project": featured_project,
        "featured_experiences": featured_experiences,
        "project_list": project_list,
        "tech_stack": tech_stack,
        "education_list": education_list,
        "experience": experience_list,
        "exp_by_year": exp_by_year,
    }
    return render(request, "index.html", context)


def show_technologies(request):
    tech_stack = TechStack.objects.all()
    raw_categories = TechStack.objects.values_list('category', flat=True).distinct()
    category_labels = {cat: TechStack.Category(cat).label for cat in raw_categories}
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "tech_stack": tech_stack,
        "category_labels": category_labels,
    }
    return render(request, "technologies.html", context)


def show_experience(request):
    experience_list = Experience.objects.all().order_by('started_at')
    raw_categories = experience_list.values_list('category', flat=True).distinct()
    category_labels = {cat: dict(Experience.EXPERIENCE_CHOICES).get(cat, cat) for cat in raw_categories}
    exp_category_labels = {val: label for val, label in Experience.EXPERIENCE_CHOICES}
    exp_by_year = OrderedDict()
    for exp in experience_list:
        year = exp.started_at.year if exp.started_at else timezone.now().year
        exp_by_year.setdefault(year, []).append(exp)
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "experience_list": experience_list,
        "exp_by_year": exp_by_year,
        "category_labels": category_labels,
        "exp_category_labels": exp_category_labels,
    }
    return render(request, "experience.html", context)





def show_projects(request):
    project_list = Project.objects.all()
    paginator = Paginator(project_list, 6)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "project_list": projects,
    }
    return render(request, "projects.html", context)
