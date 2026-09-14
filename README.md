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

Selama pengembangan proyek ini, saya pakai **Gemini** (Google AI) buat bantu debugging dan eksplorasi konsep, terutama di bagian CSS. Saya juga pakai **opencode CLI** (AI coding assistant) yang terintegrasi di terminal buat bantu analisis kode dan penulisan unit test.

AI tidak saya pakai buat ngehasilin seluruh aplikasi dari nol. Implementasi utama — mulai dari bikin model, nulis view, nulis template, sampe nulis test — saya kerjain sendiri. AI cuma saya pakai kalau saya udah stuck di masalah tertentu dan saya udah coba debug sendiri dulu.

### Strategi Prompting

Saya pakai pendekatan problem-driven prompting. Artinya saya ga pernah kasih prompt kayak "buatkan website portfolio" atau "tulis semua kode Django nya". Saya selalu identifikasi masalahnya dulu, coba debug sendiri, baru kalau beneran stuck saya tanya ke AI dengan konteks yang spesifik.

Prompt saya biasanya berisi:

1. Masalah yang saya temuin
2. Potongan kode yang bermasalah
3. Kondisi yang terjadi sekarang (apa yang keliatan di layar)
4. Hasil yang saya mau

Contoh beberapa prompt yang saya pakai waktu debugging CSS:

"ini cara biar image nya di depan nutupin tulisannya gmn dul" — ini soal z-index, saya lagi coba bikin foto nutupin teks tapi ga keliatan.

"kok masih putih gni dah" — ini waktu saya lagi debug warna background yang ga sesuai, ternyata body ketimpa sama elemen lain.

"ini dia kyknya ketimpa body deh atau ga si hero berada di bawah header tpi header transparent dan bodynya krem jdinya krem deh nah biar dia ngikut hero gmn" — ini salah satu prompt di mana saya malah koreksi jawaban AI karena solusinya ga cocok buat struktur proyek saya.

### Bagian yang Dibantu AI vs Sendiri

**Dibantu AI (debugging CSS):**

- Debuggin frontend
- Rapihin Readme.md

**Dikerjain sendiri:**

- Semua model Django (Experience, TechStack, Project, Education)
- Semua view dan logic di views.py
- Semua template HTML + Django template tags
- JavaScript (parallax, dark mode, category filter)
- Setup project, migrasi, konfigurasi settings

### Refleksi

AI itu berguna banget buat debugging CSS karena kadang saya perlu coba-coba beberapa konsep (positioning, stacking context, document flow) dan AI bisa kasih alternatif pendekatan lebih cepat dari saya googling satu-satu.

Tapi yang saya pelajari, jawaban AI ga selalu bisa langsung dipake. Kadang jawabannya bener secara teknis tapi ga cocok buat konteks proyek saya. Jadi saya tetep harus paham konsep dasarnya dulu biar bisa evaluasi jawaban AI dan tau mana yang bisa dipake mana yang ga cocok.

Intinya AI itu tool yang membantu saya lebih efisien, tapi keputusan akhir dan implementasi tetep di tangan saya.

---

## Pertanyaan Reflektif

### 1. Alur Request Halaman Portfolio

Waktu pengguna buka `http://127.0.0.1:8000/experience/`, ini yang terjadi:

Request pertama kali masuk ke `myportofolio/urls.py` (URL conf proyek). Di situ ada `path("", include("main.urls"))` yang artinya semua request selain `/admin/` diteruskan ke URL conf aplikasi `main`.

Terus `main/urls.py` terima request itu dan cari pattern yang cocok. Ada `path("experience/", show_experience, name="show_experience")`, jadi dipanggilah fungsi `show_experience` di `main/views.py`.

Di dalam view, saya query data dari database pakai `Experience.objects.all().order_by('started_at')`. Django ORM ngerubah query Python ini jadi SQL (`SELECT * FROM main_experience ORDER BY started_at`). Data yang didapet diolah dulu — digrouping berdasarkan tahun, bikin category labels — terus dikirim ke template sebagai context.

Di template `experience.html`, data ditampilin pakai Django template tags. Ada `{% if experience_list %}` buat ngecek datanya ada apa engga, terus `{% for %}` buat loop data experience-nya.

Setelah dirender, view ngembaliin HTTP response berisi HTML yang udah jadi. Browser terima HTML itu, load CSS sama JS, dan tampilin halaman experience ke pengguna.

Ringkasnya: `Browser → myportofolio/urls.py → main/urls.py → show_experience view → Experience model (query database) → template render → response → Browser`

### 2. Kenapa Data Disimpan di Model, Bukan Hardcode di Template?

Kalau data ditulis langsung di template, tiap kali ada perubahan misalnya nambah pengalaman baru atau update deskripsi proyek bikin saya harus edit file template secara manual. Ini ribet dan rawan salah, apalagi kalau datanya banyak.

Dengan nyimpen di model (database), perubahan bisa dilakuin lewat Django admin tanpa harus sentuh kode. Orang lain yang ga ngerti coding pun bisa update data lewat admin. Ini jauh lebih praktis buat maintenance.

Selain itu, data di model itu terstruktur. Kalau nanti saya mau bikin fitur baru misalnya API buat mobile app atau pencarian data jadinya tinggal bangun di atas model yang udah ada. Kalau datanya hardcode di template, setiap fitur baru harus duplikasi data di banyak tempat.

Model Django juga punya validasi otomatis (field constraints, unique, max_length) yang memastikan data yang masuk valid. Template gaada.

Contoh nyatanya: waktu saya nambahin field `role` di model `Project`, saya cuma perlu tambahin di `models.py`, jalanin `makemigrations` sama `migrate`, terus update data lewat admin. Ga perlu edit template sama sekali.

### 3. Perbedaan makemigrations dan migrate

`makemigrations` itu bikin file migration baru (format Python) yang berisi rencana perubahan schema database. File ini dihasilkan dari perbandingan model sekarang sama model di migration terakhir yang udah dijalankan. File-nya disimpen di folder `main/migrations/` dan bisa di-review dulu sebelum dijalankan.

Yang penting, `makemigrations` itu cuma bikin rencana dia ga ngubah database sama sekali.

`migrate` itu yang ngeksekusi file migration ke database. Setiap kali `migrate` jalan, Django catet di tabel `django_migrations` bahwa migration itu udah diterapkan, jadi ga dijalankan dua kali.

Jadi `migrate` itu yang bener-bener ngubah schema database yaitu bikin tabel, nambah kolom, ubah constraint, dll.

Contoh: waktu saya nambahin field `role` di model `Project`:

```python
# models.py sebelumnya ga ada field role
class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.URLField()

# sesudah ditambahin
class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    role = models.CharField(max_length=150, blank=True)  # field baru
    description = models.TextField()
    thumbnail = models.URLField()
```

Harus jalanin dua-duanya:

```bash
python manage.py makemigrations  # bikin file 0007_project_role.py
python manage.py migrate          # apply ke database
```

Tanpa `makemigrations`, Django ga tau ada perubahan schema. Tanpa `migrate`, perubahan ga diterapkan ke database. Harus berurutan.
