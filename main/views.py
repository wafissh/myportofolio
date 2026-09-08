from django.shortcuts import render

from main.models import Experience, Project, TechStack


def show_main(request):
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "npm": "2506624461",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Wien Muhammad Hafizhurrohman",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_about(request):
    context = {
        "about-me-": "Halo ini ada moockup untuk awal awal jadinya ga telrlau serius sih tpai nanti bakal panjang juga",
        "download-cv-url": ".......",
        "contact-me": "....",
        "experience_list": Experience.objects.all(),
        "project_list": Project.objects.all(),
        "tech-stack": TechStack.objects.all(),
        
        
    }
    return render(request, "about.html", context)