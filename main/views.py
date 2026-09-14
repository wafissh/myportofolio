from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from collections import OrderedDict
from django.http import HttpResponse
from main.models import Experience, Project, TechStack, Education
from main.forms import ProjectForm
from django.core import serializers


def show_main(request):
    featured_project = Project.objects.filter(is_featured=True).first()
    featured_experiences = Experience.objects.filter(is_featured=True).order_by(
        "-started_at"
    )
    project_list = Project.objects.all()
    tech_stack = TechStack.objects.all()
    education_list = Education.objects.all().order_by("-started_at")
    experience_list = Experience.objects.all().order_by("started_at")[:4]
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
    raw_categories = TechStack.objects.values_list("category", flat=True).distinct()
    category_labels = {cat: TechStack.Category(cat).label for cat in raw_categories}
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "tech_stack": tech_stack,
        "category_labels": category_labels,
    }
    return render(request, "technologies.html", context)


def show_experience(request):
    experience_list = Experience.objects.all().order_by("started_at")
    raw_categories = experience_list.values_list("category", flat=True).distinct()
    category_labels = {
        cat: dict(Experience.EXPERIENCE_CHOICES).get(cat, cat) for cat in raw_categories
    }
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

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")



def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    project_list = Project.objects.all()
    if title_query:
        project_list = project_list.filter(title__icontains=title_query)
    paginator = Paginator(project_list, 6)
    page = request.GET.get("page")
    projects = paginator.get_page(page)
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")
