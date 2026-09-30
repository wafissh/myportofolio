from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from collections import OrderedDict
from django.http import JsonResponse
from main.models import Experience, Project, TechStack, Education
from main.forms import ProjectForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime
from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie


def can_create(user):
    return user.is_authenticated and user.is_superuser


def can_update(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name__iexact="editor").exists()
    )


def can_delete(user):
    return can_create(user)

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    
    
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
        "last_login": last_login
    }
    return render(request, "index.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response





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

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not can_delete(request.user):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
    return redirect("main:show_projects")



@ensure_csrf_cookie
def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.order_by("-id")
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    paginator = Paginator(projects, 6)
    project_list = paginator.get_page(request.GET.get("page") or 1)

    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "project_list": project_list,
        "title_query": title_query,
        "can_edit": can_update(request.user),
        "can_create": can_create(request.user),
        "can_delete": can_delete(request.user),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/")
def create_project(request):
    if not can_create(request.user):
        raise PermissionDenied
    
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


@require_POST
def create_project_ajax(request):
    if not can_create(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_update(request.user):
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()

    projects = Project.objects.prefetch_related(
        "starred_by", "tech_stacks"
    ).order_by("-id")
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    paginator = Paginator(projects, 6)
    page_obj = paginator.get_page(request.GET.get("page") or 1)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in page_obj.object_list:
        starred_users = project.starred_by.all()
        is_starred = (
            request.user.is_authenticated and request.user in starred_users
        )
        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "slug": project.slug,
                "role": project.role,
                "description": project.description,
                "is_featured": project.is_featured,
                "thumbnail_url": project.get_thumbnail_url,
                "project_url": project.project_url or "",
                "tech_stacks": [tech.name for tech in project.tech_stacks.all()],
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(
                    user.username for user in starred_users
                ),
            },
        })

    response = JsonResponse(data, safe=False)
    response["X-Total-Pages"] = str(paginator.num_pages)
    response["X-Current-Page"] = str(page_obj.number)
    return response


@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")
