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

Ada 52 test cases 

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

Untuk tugas 6 ini saya sebenarnya tidak terlalu bergantung AI karena setelah tutorial 6, banyak checkbox di tugas 6 sudah kelar jadi saya cuman finishing yg gaada di tutorial 6.

- Tolong rapihkan jawaban saya ke dalam bentuk read.me yang rapih (sayya memberi input jawaban tugas refleksi menurut pemahamana saya lalu AI mmemberi tambahan dan sekaligus merapihkan)
- 

### Tugas Refleksi
### Tugas 6

1. **Apa itu REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut API sebagai RESTful?**
REST (Representational State Transfer) adalah arsitektur perangkat lunak untuk sistem terdistribusi yang menggunakan protokot HTTP standar. Mengembalikan JSON saja belum cukup karena API RESTful harus mematuhi semantik HTTP lengkap: menggunakan metode HTTP yang tepat (GET, POST, PUT, PATCH, DELETE), mengembalikan status kode yang sesuai (201 dibuat, 400 input salah, 403 dilarang, 404 tidak ditemukan, 204 dihapus), URL yang mengacu pada resource, dan optionally hypermedia (HATEOAS). Hanya mengirim JSON tanpa status code atau verb HTTP tepat dianggap "JSON API" tetapi tidak harus RESTful.

2. **Perbedaan PUT dan PATCH serta kapan masing-masing digunakan?**
- **PUT**: Mengganti seluruh representasi resource. klien mengirimkan semua field resource; server mengganti entitas lama dengan yang baru. Idempotent (memanggil ulang menghasilkan sama hasil). Digunakan ketika ingin mengganti resource sepenuhnya atau memastikan semua field diperbarui.
- **PATCH**: Modifikasi parsial resource. Menerapkan set perubahan (seperti JSON Patch/RFC 6902) pada resource yang ada. Bukan harus idempotent. Digunakan ketika hanya perlu memperbarui satu atau beberapa field tanpa mengirim seluruh resource.

3. **Peran serializer pada Django REST Framework dan keuntungan dibanding manual dictionary + JsonResponse**
- Serializer menangani validasi input (tipe field, wajib diisi, metode `validate_<field>`), deserialisasi (konversi JSON masuk ke objek Python), serialisasi (model ke JSON), representasi kustom (method fields seperti `get_star_count`), error terstruktur, penolakan otomatis 400, field read-only, dan pengelolaan relasi. Membangun dictionary secara manual melewatkan validasi, repetitive, rentan kesalahan tipe data, dan tidak menangani kasus seperti stripping HTML (XSS) atau pengecualian field sensitif.

4. **Perbedaan autentikasi dan otorisasi pada Django REST Framework, dan harus diperiksa di server, bukan hanya di template?**
- **Autentikasi**: Mengidentifikasi siapa pengguna (misal SessionAuthentication menggunakan cookie sesi). Menjawab "Siapa ini?"
- **Otorisasi**: Menentukan apakah pengguna boleh melakukan aksi tersebut (misal `IsPortfolioOwnerOrEditorOrReadOnly`). Menjawab "Apakah boleh?"
- Harus dicek di server karena template hanya pengaturan UI; pengguna bisa langsung mengakses endpoint API via curl/Postman melewati tombol yang disembunyikan. Keamanan harus ditenanggu server-side.

5. **Mengapa permintaan ubah data tetap memerlukan token CSRF saat API memakai SessionAuthentication, dan mengapa `force_authenticate` tidak cukup bukti perlindungan CSRF?**
- Django memaksa token CSRF untuk POST/PUT/PATCH/DELETE untuk mencegah Cross-Site Request Forgery (request dari situs lain menggunakan sesi korban). `force_authenticate` hanya mensimulasikan pengguna autentik tetapi tidak menyertakan token CSRF yang valid di cookie/headers; server akan menolak 403 jika token hilang. Test dengan `APIClient(enforce_csrf_checks=True)` dan `.login()` membuktikan bahwa tanpa token CSRF, permintaan ditolak, menunjukkan bahwa perlindungan CSRF berjalan secara independen dari autentikasi.
