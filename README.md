# myportofolio

Nama: Wien Muhammad Hafizhurrohman
NPM: 2506624461
Kelas: PBP E

## Tentang Proyek

Ini adalah website portfolio pribadi yang dibikin buat tugas PBP. Isinya profil diri, pengalaman kerja/organisasi, proyek yang pernah dikerjain, tech stack yang dikuasai, sama riwayat pendidikan. Dibangun pakai Django 6.1, jadi semuanya server-side rendering pakai Django template, ga pake framework frontend macem React atau Vue.

## Tech Stack

- Django 6.1 (backend)
- SQLite3 (database waktu development)
- PostgreSQL (database waktu production, via psycopg2-binary)
- WhiteNoise (static files serving di production)
- Gunicorn (WSGI server buat deployment)
- python-dotenv (buat manage environment variable)

## Struktur Folder

```
myportofolio/
├── manage.py
├── requirements.txt
├── .env
├── .env.prod
├── myportofolio/          # project package (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/                  # aplikasi utama
│   ├── models.py          # model: Experience, TechStack, Project, Education
│   ├── views.py           # 4 view functions buat 4 halaman
│   ├── urls.py            # URL routing
│   ├── admin.py
│   └── tests.py           # 13 unit test cases
├── templates/
│   ├── index.html         # halaman utama / profil
│   ├── experience.html    # timeline pengalaman
│   ├── technologies.html  # grid tech stack
│   └── projects.html      # daftar proyek
└── static/
    ├── css/style.css
    ├── js/app.js
    └── img/
```

## Model

Ada 4 model di aplikasi `main`:

- **Experience** — buat nyimpen pengalaman kerja/organisasi. Field-nya: title, description, category (internship, volunteer, part-time, full-time, freelance, organization), thumbnail, is_featured, started_at, ended_at.
- **TechStack** — teknologi yang dikuasai. Ada name (unique), category (BACKEND, DATABASE, API, FRONTEND, CLOUD, DEVOPS, AI_ML, LANGUAGE), sama icon_class buat icon devicon.
- **Project** — proyek portofolio. Ada title, slug (unique), role, description, thumbnail, project_url, is_featured, dan relasi many-to-many ke TechStack.
- **Education** — riwayat pendidikan. Field-nya title, started_at, ended_at, education_loc.

## Cara Setup

1. Clone repo ini
2. Buat virtual environment: `python -m venv venv`
3. Aktifkan venv:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Bikin file `.env` di root, isi: `PRODUCTION=False`
6. Jalankan migrasi: `python manage.py migrate`
7. (Opsional) Bikin superuser: `python manage.py createsuperuser`

## Menjalankan Server

```bash
python manage.py runserver
```

Buka `http://127.0.0.1:8000/`

Halaman yang ada:

- `/` — profil utama, featured project, experience ringkas, education, tech marquee
- `/experience/` — timeline pengalaman lengkap + filter kategori
- `/technologies/` — grid tech stack + filter
- `/projects/` — daftar proyek, ada pagination 6 item per halaman

## Unit Tests

Jalankan: `python manage.py test main`

Ada 13 test cases yang nge-cover 3 skenario utama buat tiap view:

1. URL bisa diakses dan pake template yang bener
2. Data dari model muncul di halaman HTML kalau ada data
3. Halaman nampilin pesan empty state kalau datanya kosong

Detailnya:

- MainViewTest (3 test) — ngecek `/` pake `index.html`, data semua model muncul, empty state
- ExperienceViewTest (3 test) — ngecek `/experience/` pake `experience.html`, data experience muncul, empty state
- TechnologiesViewTest (3 test) — ngecek `/technologies/` pake `technologies.html`, data tech stack muncul, empty state
- ProjectsViewTest (3 test) — ngecek `/projects/` pake `projects.html`, data project muncul, empty state
- NonexistentPageTest (1 test) — ngecek URL yang ga ada balik 404

## Fitur

- Responsive — layout nya ngikutin ukuran layar
- Dark Mode — ada tombol switch buat ganti mode terang/gelap (di app.js)
- Parallax Clouds — efek parallax di section hero pake layer awan
- Category Filtering — bisa filter experience dan tech stack berdasarkan kategori
- Pagination — navigasi halaman di daftar proyek
- Featured Items — ada penanda khusus buat project dan experience yang unggulan
- Admin Panel — bisa akses `/admin/` buat manage data lewat Django admin

---

## AI Disclosure

### Tools yang Dipake

Selama pengembangan proyek ini, saya pakai **Gemini** (Google AI) buat bantu debugging dan eksplorasi konsep, terutama di bagian CSS.

AI tidak saya pakai buat ngehasilin seluruh aplikasi dari nol. Implementasi utama — mulai dari bikin model, nulis view, nulis template, sampe nulis test — saya kerjain sendiri. AI cuma saya pakai kalau saya udah stuck di masalah tertentu dan saya udah coba debug sendiri dulu.

### Strategi Prompting

Untuk tugas 4 ini saya sebenarnya tidak terlalu bergantung AI karena setelah tutorial 4, banyak checkbox di tugas 4 sudah kelar jadi saya cuman finishing seperti update yg gaada di tutorial 4.

Menanyakan cara memasukkan user ke dalam salah satu group di Django.
Menanyakan cara menerapkan pembatasan hak akses di sisi server (server-side check) sesuai 4 peran/role (mengalihkan ke login jika belum masuk, serta mengembalikan HTTP 403 Forbidden untuk aksi yang dilarang).

Menanyakan kebenaran dari potongan kode pengecekan kondisi: if not request.user.is_superuser or request.user.is_editor: raise PermissionDenied

Verifikasi Sintaks Django Template ({% if %}): {% if user.is_superuser or request.user.groups.filter(name='editor').exists() %}



