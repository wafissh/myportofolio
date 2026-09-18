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

Untuk tugas 3 ini saya sebenarnya tidak terlalu bergantung AI karena setelah tutorial 3, banyak checkbox di tugas 3 sudah kelar jadi saya cuman finishing seperti update yg gaada di tutorial 3.

- Bantu aku menjawab pertanyaan ini dan jelaskan secara detail(pertanyaan reflektif)
- Gimana cara nampilin json dari model ke html.

### Bagian yang Dibantu AI vs Sendiri

**Dibantu AI (debugging CSS):**

- Debuggin frontend
- Rapihin Readme.md
- Bantu jawab pertanyaan reflektif

**Dikerjain sendiri: Tugas 3**

- CRUD(update,delete)
- MVT Tugas 3

- S

### Refleksi

AI itu berguna banget buat debugging CSS karena kadang saya perlu coba-coba beberapa konsep (positioning, stacking context, document flow) dan AI bisa kasih alternatif pendekatan lebih cepat dari saya googling satu-satu.

Tapi yang saya pelajari, jawaban AI ga selalu bisa langsung dipake. Kadang jawabannya bener secara teknis tapi ga cocok buat konteks proyek saya. Jadi saya tetep harus paham konsep dasarnya dulu biar bisa evaluasi jawaban AI dan tau mana yang bisa dipake mana yang ga cocok.

Intinya AI itu tool yang membantu saya lebih efisien, tapi keputusan akhir dan implementasi tetep di tangan saya, AI juga membantu saya untuk hal hal yang saya kurang pahami ibarat menjadi sebuah search engine.

---

## Pertanyaan Reflektif

### 1. Kenapa Menggunakan ModelForm Alih-alih Form HTML Manual?

ModelForm pada Django adalah class yang secara otomatis membuat form HTML berdasarkan field-field yang ada di model Django. Ada beberapa alasan kenapa ModelForm lebih baik daripada nulis form HTML manual:

**Otomatisasi dan DRY (Don't Repeat Yourself).** Dengan ModelForm, saya cukup definisikan model di `models.py` dan ModelForm akan otomatis generate field, input type, label, dan validasi sesuai definisi model. Kalau pakai form manual, saya harus nulis ulang semua info itu di HTML — redundan dan rawan inconsistensi. Misalnya, kalau model punya field `CharField(max_length=100)`, ModelForm otomatis nambahin atribut `maxlength="100"` di input HTML-nya.

**Validasi bawaan.** ModelForm mewarisi validasi dari field-field model Django — `max_length`, `unique`, `blank`, `null`, `choices`, dan custom `clean_*` methods. Jadi saya ga perlu nulis validasi ulang di form. Kalau form manual, semua validasi harus ditulis sendiri, baik di sisi client (JavaScript) maupun server (view).

**Keamanan.** ModelForm secara otomatis handle sanitasi input dan mencegah SQL injection karena berinteraksi lewat ORM, bukan query mentah.

**Maintainability.** Kalau saya mau nambah atau ubah field di model, saya cuma perlu update model dan ModelForm akan menyesuaikan otomatis. Form manual harus diupdate di dua tempat (model dan HTML) secara terpisah.

`{% csrf_token %}` adalah Django template tag yang menghasilkan input tersembunyi berisi token keamanan CSRF (Cross-Site Request Forgery). Kenapa ini wajib?

**Apa itu CSRF?** CSRF adalah serangan di mana situs jahat memanfaatkan session cookie yang tersimpan di browser pengguna. Misalnya, pengguna login di bank.com, lalu mengunjungi situs jahat yang secara diam-diam mengirim request ke bank.com dengan endpoint transfer uang. Karena browser otomatis lampirkan session cookie, bank.com mengira request itu legitimate.

**Cara kerja CSRF token.** Django menyimpan token rahasia di session pengguna, lalu mengirimkan token yang sama ke template via `{% csrf_token %}`. Saat form disubmit, token dikirim balik ke server. Django membandingkan token dari form dengan token di session. Kalau cocok, request diterima. Kalau ga cocok atau ga ada, request ditolak (403 Forbidden). Karena token ini unik per session dan tidak bisa diprediksi, situs jahat tidak bisa memalsukannya.

**Kenapa di-Django wajibkan?** Django menerapkan defense-in-depth. Bahkan kalau ada mekanisme keamanan lain, CSRF tetap menjadi lapisan proteksi tambahan yang krusial untuk semua POST/PUT/DELETE request.

### 2. Kenapa JSON Lebih Disukai dibanding XML dalam Pengembangan Web Modern?

**Ukuran dan efisiensi.** JSON lebih ringkas. Sebuah data yang diwakili dalam JSON biasanya jauh lebih kecil ukurannya dibanding XML. Misalnya, `{"name": "Hafiz"}` vs `<name>Hafiz</name>`. Tanpa closing tags dan tanpa atribut-atribut tambahan, JSON menghemat bandwidth dan mempercepat transfer data.

**Struktur data lebih fleksibel.** JSON mendukung array, object, nested object, null, boolean, dan number secara native. XML harus mensimulasikan array dengan repeated tags atau atribut khusus.

### 3. Alur Mengembalikan Data Portofolio dalam Bentuk JSON dan Peran Serialization

**Alur yang terjadi saat view mengembalikan JSON:**

1. **Request masuk.** Pengguna atau client (bisa browser, mobile app, atau API consumer) mengirim HTTP request ke endpoint tertentu, misalnya `/api/projects/`.

2. **URL routing.** Django URLconf menangkap request dan mencocokkan pattern. Jika ada `path("api/projects/", get_projects_json)`, maka fungsi view `get_projects_json` dipanggil.

3. **Query database.** Di dalam view, Django ORM mengeksekusi query ke database:

   ```python
   projects = Project.objects.all()
   ```

   ORM menerjemahkan ini menjadi SQL: `SELECT * FROM main_project`.

4. **Serialization.** Data queryset berupa objek-objek Python (Python objects) tidak bisa langsung diubah menjadi JSON. Objek Python memiliki atribut yang kompleks — field model, methods, relasi, datetime objects — yang tidak bisa di-serialize secara langsung. Di sinilah serializer berperan:

   ```python
   from django.http import JsonResponse
   from django.core.serializers import serialize

   data = serialize("json", projects)
   ```

   Atau dengan serializer manual:

   ```python
   projects_data = list(projects.values("title", "slug", "description", "role", "is_featured"))
   return JsonResponse({"projects": projects_data})
   ```

   Serializer mengubah objek-objek Python menjadi struktur data yang bisa di-convert ke JSON (list, dict, string, number, boolean, null).

5. **Response.** `JsonResponse` membungkus data dalam format JSON dengan header `Content-Type: application/json` dan mengirimkannya kembali ke client.

6. **Client menerima.** Client mem-parsing JSON response dan mengolahnya — misalnya menampilkan di UI, memproses di mobile app, atau menampilkan di dashboard.

**Mengapa serialization diperlukan?**

- **Objek Python bukan JSON.** Objek model Django punya method, property, dan referensi ORM yang tidak bisa dikonversi langsung ke JSON. Serializer "memecah" objek menjadi kumpulan key-value pairs yang JSON-compatible.
- **Keamanan.** Serialization memungkinkan kita mengontrol field mana yang boleh diekspos. Tidak semua field model harus dikirim ke client (misalnya field `is_admin` atau `password`). Serializer menjadi filter antara data internal dan data publik.
- **Menghindari circular reference.** Model Django bisa punya relasi ForeignKey atau ManyToMany yang saling merujuk. Tanpa serializer yang proper, konversi langsung ke JSON akan error karena circular reference.
- **Standarisasi.** Serializer memastikan format output konsisten dan terprediksi, sehingga client selalu menerima data dengan struktur yang sama.
