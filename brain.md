# BRAIN.md — Little Light Sekolah Kristen Lentera Ambarawa

## 1. Identitas & Tujuan

**Little Light – Sekolah Kristen Lentera Ambarawa** adalah platform digital sederhana untuk anak sekolah Kristen. Fokusnya adalah menjadi tempat untuk menonton renungan anak, membaca Alkitab literasi, mendengarkan Alkitab bersuara, dan membaca renungan harian.

Prinsip utama:

> Website adalah katalog, pemutar, dan pembaca. Google Drive tetap menjadi master/source file.

Platform tidak dimaksudkan menjadi media sosial.

---

## 2. Jenis Konten

### Renungan Video (Little Light Puppet Show)
Video renungan berbasis lakon sandiwara boneka edukasi karakter Kristen:
- **Karakter Utama**:
  - **Guneo**: Anak laki-laki lincah (7-8 tahun), energik, sedikit usil, polos, bicara cepat.
  - **Lili**: Anak perempuan lembut (7-8 tahun), manis, ramah, penuh empati.
  - **Joana**: Kakak perempuan bijak (9-10 tahun), percaya diri, tegas, penyampai ayat Alkitab dan penuntun teman-temannya.
- **Aturan Deskripsi & Sinopsis**: Wajib bersumber langsung dari naskah resmi (`.docx`), mencantumkan ayat Alkitab dan konflik nyata per episode (misal: mainan robot disita guru, pura-pura tidak dengar saat main bola di kala mendung, ambil penghapus stroberi teman, debu disapu ke bawah karpet).
- Untuk browser: delivery MP4 H.264/AAC (+faststart). MOV asli disimpan di arsip master.

### Alkitab Literasi (3D Claymation)
Cerita Alkitab bergambar untuk anak PAUD/TK dan Fase A:
- **Prinsip Karakter**: **MURNI TOKOH & PERISTIWA ALKITAB SAJA**. Tidak ada tokoh fiktif tambahan (TIDAK ADA Dito & Hana). Konten 100% setia pada narasi Alkitab (Tuhan Yesus, para nabi, kisah Alkitab).
- **Format Visual**: 3D Claymation dengan tata letak *Open Book Spread* (kiri: karya seni tanah liat 3D adegan Alkitab penuh warna; kanan: kertas gading teks cerita firman Tuhan yang disederhanakan untuk anak).
- Menggunakan PDF.js reader dengan dukungan zoom, fullscreen, dan flipbook-friendly layout.

### Alkitab Bersuarа
Audio Alkitab dengan player, progress, volume, next/previous, playlist, resume, dan mini-player.

### Renungan Harian (Fase B & C)
Buku renungan siswa kelas 3–6 SD:
- Berupa 1 file Master PDF utuh per tahun ajaran.
- Disajikan per minggu menggunakan mekanisme **Virtual Page Range** (Opsi A) melalui tabel database `devotion_ranges`.


---

## 3. Konsep User Experience

Home harus berorientasi pada **Hari Ini**, bukan sekadar daftar upload terbaru.

Contoh:

```text
LITTLE LIGHT

Hari Ini
- Bacaan Alkitab
- Alkitab Bersuarа
- Renungan Anak
- Renungan Fase B
- Renungan Fase C

Lanjutkan Perjalananmu
Playlist
Materi Terbaru
```

Navigasi:

```text
HOME
├── RENUNGAN VIDEO
├── ALKITAB LITERASI
├── ALKITAB BERSUARA
└── RENUNGAN HARIAN
    ├── FASE B
    └── FASE C
```

Fitur yang sengaja tidak dibuat pada MVP:
- komentar
- like
- follower
- chat/DM
- upload user
- social feed
- forum
- monetisasi
- live streaming kompleks

---

## 4. Playlist

Playlist disimpan di database, bukan bergantung pada struktur folder Drive.

Contoh:

```text
Renungan Anak — September 2026
├── Week 1 — Hatiku Tanah yang Subur
├── Week 2 — Nasihat itu Tanda Sayang
├── Week 3 — Buku Petunjuk Hebat
└── Week 4 — Jangan Cuma Hafal, Ayo Lakukan!
```

Tabel yang disarankan:
- `playlists`
- `playlist_items` dengan `sort_order`

---

## 5. Arsitektur Utama

```text
GOOGLE DRIVE
Master Media
     │
     │ Scan / Metadata
     ▼
GOOGLE APPS SCRIPT
Sync / Automation
     │
     ▼
SUPABASE
PostgreSQL / Auth / RLS / Metadata
     │
     ├──────────────┐
     ▼              ▼
ADMIN APP        USER APP
Private          Public/read-only
     │              │
     │              ▼
     │        Video / PDF / Audio
     │              │
     └──────────────┴──→ Media Delivery
                         Google Drive initially
                         CDN/Object Storage later
```

Keputusan arsitektur:
- Google Drive = master storage.
- Supabase = database/backend/auth/RLS/catalog.
- GAS = scanner/sync/automation.
- Admin App = pengelolaan konten.
- User App = konsumsi konten.
- Jangan menggunakan GAS sebagai server/proxy video.

---

## 6. Dua Aplikasi

### Admin App
Contoh:
`manage.lentera.org`

Fungsi:
- login
- dashboard
- scan Google Drive
- add content
- edit metadata
- review
- approve
- publish
- unpublish
- playlist
- daily schedule
- audit log
- operator management

### User App
Contoh:
`littlelight.lentera.org`

Fungsi:
- home
- video player
- PDF reader
- audio player
- renungan
- playlist
- search
- daily content

User App tidak boleh mempunyai:
- upload
- edit
- delete
- scan Drive
- approve
- publish
- admin tools

---

## 7. Workflow Konten

File di Drive **tidak otomatis menjadi publik**.

Workflow:

```text
Google Drive
   ↓
SCAN
   ↓
DRAFT
   ↓
REVIEW
   ↓
APPROVED
   ↓
PUBLISHED
   ↓
USER APP
```

Status yang disarankan:
- DRAFT
- REVIEW
- APPROVED
- PUBLISHED
- ARCHIVED
- REJECTED

Emergency unpublish:

```text
PUBLISHED
   ↓
Emergency Unpublish
   ↓
published = false
   ↓
Tidak tampil di User App
```

File master di Drive tidak perlu dihapus.

---

## 8. Role

### OPERATOR
Boleh:
- scan
- add content
- edit metadata
- membuat playlist
- mengajukan konten

Tidak boleh:
- publish final
- mengubah role
- melakukan tindakan kritis tertentu

### ADMIN
Boleh:
- approve
- publish
- unpublish
- archive
- mengelola operator
- melihat audit log
- mengelola konfigurasi

Alur:

```text
OPERATOR → DRAFT/REVIEW → ADMIN → PUBLISHED → USER
```

---

## 9. Audit Log

Catat tindakan penting:

```text
actor
action
entity_type
entity_id
before_data
after_data
reason
created_at
```

Contoh:
- operator menambahkan video
- admin menyetujui
- admin mempublikasikan
- admin melakukan unpublish
- operator mengubah judul

---

## 10. Struktur Google Drive

Disarankan:

```text
LITTLE LIGHT
├── 01 - RENUNGAN VIDEO
├── 02 - ALKITAB LITERASI
├── 03 - ALKITAB BERSUARA
├── 04 - RENUNGAN HARIAN
│   ├── FASE B
│   └── FASE C
├── 05 - THUMBNAILS
└── 99 - ARSIP
```

Namun database aplikasi tetap menjadi sumber kebenaran untuk status dan klasifikasi. Jangan membuat aplikasi bergantung secara kaku pada folder Drive.

---

## 11. Drive Scanner

Admin App memiliki tombol **Scan Google Drive**.

Scanner mengambil:
- file ID
- filename
- MIME type
- ukuran
- tanggal
- URL
- metadata
- jenis media

Scanner dapat membaca pola filename.

Contoh:

```text
3-September 2026_Week 2_Nasihat itu Tanda Sayang.mov
```

diparsing menjadi:

```text
date  = 2026-09-03
week  = 2
title = Nasihat itu Tanda Sayang
type  = video
```

Hasil scan selalu dibuat sebagai DRAFT agar operator/admin dapat mengoreksi metadata.

---

## 12. Add Content Wizard

Operator juga dapat memasukkan URL Google Drive:

```text
Google Drive URL
[________________]

[Detect File]
```

Sistem mengambil:
- Drive File ID
- filename
- MIME type
- size
- preview jika tersedia

Operator mengisi:
- type
- category
- date
- week
- phase
- playlist
- description
- thumbnail

Kemudian **Save as Draft**.

---

## 13. Database

### `media`

```text
id
drive_file_id
drive_url
title
description
media_type
mime_type
file_size
duration
date
week
phase
thumbnail_url
status
published
published_at
created_by
approved_by
created_at
updated_at
```

Gunakan `drive_file_id` sebagai identitas file, bukan filename, karena filename dapat berubah.

### `playlists`

```text
id
title
description
thumbnail_url
status
created_by
created_at
updated_at
```

### `playlist_items`

```text
id
playlist_id
media_id
sort_order
```

### `daily_readings`

```text
id
date
bible_reference
pdf_media_id
audio_media_id
phase_b_devotion_id
phase_c_devotion_id
created_at
updated_at
```

### `devotion_ranges` (Virtual Page Range Opsi A)

Tabel untuk memetakan 1 master PDF lengkap ke dalam minggu-minggu renungan siswa tanpa memotong file fisik:

```text
id
media_id            (relasi ke media master PDF di Google Drive)
phase               ('fase_b' atau 'fase_c')
week_number         (integer, misal: 1 s.d. 36)
start_page          (nomor halaman awal di file PDF, misal: 1)
end_page            (nomor halaman akhir di file PDF, misal: 12)
title               (judul tema minggu terkait)
bible_verse         (ayat bacaan Alkitab)
theme               (tema bulanan/tahunan)
created_at
updated_at
```

### `profiles`

```text
id
name
email
role
active
created_at
updated_at
```

Role:
- operator
- admin

### `audit_logs`

```text
id
actor_id
action
entity_type
entity_id
before_data
after_data
reason
created_at
```

### Opsional `sync_logs`

```text
id
started_at
finished_at
files_scanned
files_added
files_updated
errors
status
error_message
```

---

## 14. RLS / Security

User App hanya boleh membaca konten published.

Konsep:

```text
SELECT media
WHERE published = true
```

User tidak boleh:
- INSERT
- UPDATE
- DELETE

Admin/Operator menggunakan Supabase Auth dan RLS sesuai role.

**Jangan pernah menaruh Supabase Service Role Key di frontend.**

Credential Google Drive/OAuth juga tidak boleh dikirim kepada pengguna publik.

---

## 15. Daily Content Engine

Fitur penting:

> “Apa yang harus saya lakukan hari ini?”

Tabel `daily_readings` memetakan:

```text
DATE
 ↓
Bible reading
 ↓
Audio
 ↓
Video
 ↓
Fase B
 ↓
Fase C
```

Contoh Home:

```text
Kamis, 8 Oktober 2026

Hari Ini

Bacaan Alkitab
[Read]

Alkitab Bersuarа
[Play]

Renungan
[Watch]

Fase B
[Read]

Fase C
[Read]
```

---

## 16. Google Apps Script

GAS cocok untuk:
- scan Drive
- metadata
- sync database
- scheduled jobs
- triggers
- parsing filename
- maintenance

GAS tidak cocok sebagai video streaming proxy.

Hindari:

```text
Browser
 ↓
GAS
 ↓
Download full video
 ↓
GAS
 ↓
Browser
```

Alasannya:
- execution resource
- bandwidth
- bottleneck
- tidak cocok sebagai CDN

Prinsip:
**GAS = automation/sync engine, bukan media server.**

---

## 17. Google Drive API

Drive API dapat digunakan untuk:
- `files.list`
- `files.get`
- search
- metadata
- download
- partial/range download

Drive API memiliki quota per project/per user. Error 403/429 dapat muncul saat quota terlampaui.

Referensi resmi:
- https://developers.google.com/workspace/drive/api/guides/limits
- https://developers.google.com/workspace/drive/api/guides/manage-downloads
- https://developers.google.com/workspace/drive/api/guides/search-files

Quota harus diverifikasi ulang sebelum production karena kebijakan dapat berubah.

---

## 18. Media Delivery — Risiko Teknis Terbesar

Pertanyaan paling penting bukan database, tetapi:

> Bagaimana browser mengambil video/PDF/audio dari Google Drive secara aman dan stabil?

Yang harus diuji:
- permission
- public/private access
- OAuth
- CORS
- HTTP Range
- streaming
- large files
- concurrent users
- browser compatibility
- download behavior

Jangan mengasumsikan URL Google Drive pasti dapat langsung digunakan dalam `<video>`.

---

## 19. Media Proof of Concept

Sebelum membangun seluruh aplikasi, gunakan:
- 1 video sekitar 100–200 MB
- 1 PDF besar
- 1 audio

Uji:
- Chrome desktop
- Android Chrome
- iPhone/Safari bila tersedia
- WiFi
- seluler
- beberapa pengguna bersamaan

Uji:
- play
- pause
- seek
- resume
- range
- loading
- error
- fullscreen
- PDF zoom
- page navigation

Ini harus dilakukan sebelum production.

---

## 20. Bandwidth

Contoh:

```text
Video = 138 MB
Viewer = 1.000
```

Jika seluruh video ditonton:

```text
138 MB × 1.000 ≈ 138 GB
```

Kesimpulan:
jangan menjadikan GAS atau Supabase sebagai proxy media besar jika Google Drive dapat menjadi sumber delivery.

---

## 21. Supabase

Supabase cocok untuk:
- PostgreSQL
- Auth
- RLS
- metadata
- workflow
- Edge Functions jika diperlukan

Jangan otomatis memindahkan semua video ke Supabase Storage jika Drive tetap menjadi master, karena egress/bandwidth dapat menjadi beban.

Referensi:
- https://supabase.com/docs/guides/platform/billing-on-supabase
- https://supabase.com/docs/guides/database/overview

---

## 22. Scale

Google Drive bukan CDN khusus.

Untuk tahap awal sekolah, solusi Drive dapat dicoba jika hasil prototype stabil.

Jika pengguna berkembang:

```text
Google Drive (Master)
        ↓
Object Storage / Media Layer
        ↓
CDN
        ↓
User
```

Database tetap Supabase.

Jangan menganggap angka concurrent user tertentu sebagai jaminan resmi. Lakukan load test.

---

## 23. Storage Abstraction

Jangan membuat database hanya bergantung pada satu field URL.

Lebih baik:

```text
storage_provider
storage_file_id
storage_url
```

Contoh sekarang:

```text
storage_provider = google_drive
```

Masa depan dapat berubah menjadi:

```text
storage_provider = r2
```

atau storage lain.

Dengan demikian migrasi media tidak membutuhkan rebuild aplikasi.

---

## 24. PDF

Gunakan PDF.js untuk:
- zoom
- page navigation
- search
- fullscreen
- large PDF
- lazy/range loading bila delivery mendukung

Tetap uji CORS/range/authorization terhadap Google Drive.

### SOP Virtual Page Range (Opsi A — Master PDF Tunggal)
Untuk Renungan Fase B dan Fase C yang hanya memiliki 1 file PDF lengkap tahunan:
1. File PDF master tetap 1 utuh di Google Drive (`04 - RENUNGAN HARIAN`).
2. Web Viewer (PDF.js) membaca URL master tersebut dengan header Range Request (`disableRange: false`).
3. Ketika siswa mengklik minggu tertentu (misal: Minggu 2), modul viewer langsung mengunci:
   - `currentPage = range.start_page`
   - Batas minimum: `range.start_page`
   - Batas maksimum: `range.end_page`
4. Di mata siswa, nomor halaman yang tampil adalah halaman bab minggu tersebut, sehingga anak tidak tersesat atau terbebani ratusan halaman lain.
5. Guru/Operator cukup menginput daftar rentang halaman di Admin CMS (`devotion_ranges`).


---

## 25. Video

Rekomendasi delivery:
- MP4
- H.264
- AAC

Master:
- MOV asli tetap di Drive.

Konsep:

```text
Original MOV
 ↓
Drive Master
 ↓
Transcode
 ↓
MP4 Delivery
```

---

## 26. Audio

Player harus memiliki:
- play/pause
- seek
- duration
- volume
- next/previous
- playlist
- resume
- mini-player

---

## 27. Mobile First / PWA

Prioritas:

```text
Mobile → Tablet → Desktop
```

UI:
- tombol besar
- teks jelas
- navigasi minim
- cepat
- ramah anak

PWA dapat ditambahkan:
- Add to Home Screen
- icon
- manifest
- service worker
- app-like experience

Offline media tidak menjadi prioritas awal.

---

## 28. Child-Safe Design

Karena targetnya anak:
- tanpa chat
- tanpa DM
- tanpa komentar publik
- minim tracking
- minim pengumpulan data
- tidak ada upload user
- tidak ada fitur sosial yang tidak diperlukan

Prinsip:
**Child-safe by design.**

Analytics sebaiknya lebih banyak berupa statistik agregat seperti:

```text
Video A
Views: 312
Completion: 72%
```

daripada profil detail anak.

---

## 29. Admin Dashboard

Contoh:

```text
LITTLE LIGHT ADMIN

Draft       12
Review       4
Published  126
Archived    32

[Scan Google Drive] [Add Content]
```

Menu:
- Dashboard
- Content
- Playlists
- Daily Schedule
- Drive Scanner
- Review Queue
- Published
- Archive
- Operators
- Audit Log
- Settings

---

## 30. User App

Home:

```text
Hari Ini
────────────
Bacaan Hari Ini
Alkitab Bersuarа
Renungan Anak
Fase B
Fase C

Lanjutkan
Playlist
Materi Terbaru
```

Search:
- title
- description
- week
- date
- category
- phase
- playlist

---

## 31. UX Video

Player:

```text
┌─────────────────────────┐
│                         │
│          VIDEO          │
│                         │
├─────────────────────────┤
│ ▶ 03:21 / 08:42        │
│ ━━━━━━━━━━━━━━━         │
└─────────────────────────┘

Judul
Week 2 · September 2026

[← Sebelumnya] [Berikutnya →]
```

---

## 32. UX PDF

```text
← Alkitab Literasi

       PDF PAGE

− 100% +    12 / 248    ⛶
```

---

## 33. UX Audio

```text
┌─────────────────────────────┐
│ ▶ Alkitab Bersuarа          │
│   Kejadian 1       12:34    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━   │
└─────────────────────────────┘
```

Mini-player tetap aktif ketika pindah halaman.

---

## 34. Error States

Loading:

```text
Memuat Little Light...
```

Media:

```text
Sedang memuat video...
```

Error:

```text
Maaf, materi ini sedang tidak dapat diputar.
[Coba Lagi]
```

Unpublished/removed:

```text
Materi ini sudah tidak tersedia.
```

---

## 35. Monitoring

Admin sebaiknya dapat melihat:
- last sync
- files scanned
- new files
- updated files
- errors
- draft count
- review count
- published count

Contoh:

```text
Last Drive Sync
07 Oct 2026 22:10

Files scanned: 182
New: 4
Updated: 7
Errors: 0
```

---

## 36. Struktur Repository

```text
little-light/
├── README.md
├── BRAIN.md
├── CHANGELOG.md
├── admin-app/
├── user-app/
├── gas-sync/
│   ├── Code.gs
│   ├── drive-scanner.gs
│   ├── supabase.gs
│   ├── parser.gs
│   └── config.gs
├── database/
│   ├── schema.sql
│   ├── policies.sql
│   └── seed.sql
└── docs/
    ├── architecture.md
    ├── security.md
    ├── deployment.md
    └── media-delivery.md
```

---

## 37. Teknologi yang Disarankan

Frontend:
- React / Next.js / Vite atau framework modern sederhana.

Backend:
- Supabase PostgreSQL
- Supabase Auth
- Supabase RLS
- Edge Functions bila diperlukan

Master storage:
- Google Drive

Automation:
- Google Apps Script

PDF:
- PDF.js

Media:
- HTML5 `<video>` dan `<audio>` dengan mekanisme delivery yang sudah diuji.

PWA:
- Web App Manifest
- Service Worker

---

## 38. Alternatif Sederhana

Prototype dapat menggunakan:

```text
Google Drive
 ↓
GAS
 ↓
Google Sheets
 ↓
User App
```

Namun untuk production dengan:
- role
- audit
- approval
- RLS
- relational data
- dua aplikasi

Supabase lebih cocok.

Google Sheets masih berguna untuk import/export/bulk editing/reporting.

---

## 39. MVP

Prioritas MVP:

1. User Home
2. Video Player
3. PDF Reader
4. Audio Player
5. Daily Content
6. Admin Login
7. Add Google Drive URL
8. Publish/Unpublish
9. Basic Playlist
10. Supabase Database

Setelah MVP:
- Drive Scanner
- Audit Log
- Role refinement
- Scheduling
- PWA
- Search improvement
- Analytics
- load testing

---

## 40. Development Roadmap

### Phase 0 — Architecture
- database
- RLS
- media delivery
- Drive structure
- domain

### Phase 1 — Media POC
- video
- PDF
- audio
- Drive delivery

### Phase 2 — Database
- media
- playlist
- daily_readings
- profiles
- audit_logs

### Phase 3 — Admin
- login
- dashboard
- scan
- add
- review
- publish

### Phase 4 — User
- home
- video
- PDF
- audio
- devotion
- playlist
- search

### Phase 5 — Automation
- GAS scanner
- sync
- filename parser
- scheduled jobs

### Phase 6 — Security
- RLS
- roles
- unauthorized access testing
- Drive permission
- key protection

### Phase 7 — Production
- domain
- SSL
- PWA
- monitoring
- backup
- documentation

---

## 41. Hal yang Masih Belum Final

1. My Drive atau Shared Drive?
2. Apakah file media boleh public/read-only?
3. User app tanpa login atau login?
4. Mekanisme private Drive → browser?
5. Konversi MOV → MP4?
6. PDF tetap di Drive?
7. Audio tetap di Drive?
8. Operator menggunakan Google Workspace?
9. Jumlah target user?
10. Concurrent users?
11. Domain final?
12. Analytics?
13. Apakah anak perlu akun?
14. Jadwal Fase B/C?
15. Apakah daily reading mengikuti kalender sekolah?

---

## 42. Risiko Utama

### HIGH
**Google Drive → Browser media delivery**
- CORS
- authentication
- range
- streaming
- quota
- concurrency

### MEDIUM
**MOV compatibility**
→ gunakan MP4 H.264/AAC untuk delivery.

**Drive API quota**
→ caching, incremental scan, jangan proxy media.

**Supabase egress**
→ jangan jadikan Supabase jalur streaming jika tidak perlu.

### LOW/MEDIUM
Database complexity → Supabase/PostgreSQL cukup kuat.

---

## 43. Keputusan Baseline

Keputusan yang sebaiknya tidak diubah tanpa alasan:

1. Dua aplikasi: Admin + User.
2. Google Drive sebagai master.
3. Supabase sebagai backend/database.
4. GAS sebagai sync/automation.
5. Approval workflow.
6. User App read-only.
7. PDF.js untuk PDF besar.
8. Media delivery harus dibuktikan dengan POC.
9. Simpan `storage_provider` agar storage dapat diganti.
10. Child-safe by design.

---

## 44. Next Action Paling Penting

Sebelum membangun CMS lengkap:

### Step 1
Siapkan:
- satu video MOV/MP4
- satu PDF besar
- satu audio

### Step 2
Buat prototype direct media delivery dari Google Drive.

### Step 3
Uji:
- browser desktop
- Android
- iPhone/Safari jika ada
- seek
- range
- fullscreen
- PDF navigation
- audio
- beberapa user bersamaan

### Step 4
Jika lolos, buat Supabase schema.

### Step 5
Bangun Admin MVP:

```text
Login
 ↓
Add Drive URL
 ↓
Detect metadata
 ↓
Save DRAFT
 ↓
Publish
```

### Step 6
Bangun User MVP:

```text
Home
 ↓
Published Content
 ↓
Player / Reader
```

### Step 7
Tambahkan GAS Scanner.

### Step 8
Tambahkan Daily Content.

### Step 9
Tambahkan audit/security.

### Step 10
Load test dan production deployment.

---

## 45. Prinsip Emas

### Storage ≠ Database
Drive menyimpan file; Supabase menyimpan informasi tentang file.

### Automation ≠ Media Delivery
GAS mengatur; browser mengambil media melalui delivery layer.

### Scan ≠ Publish
Scan hanya menemukan file; Admin menentukan apa yang publik.

### User ≠ Admin
User App tidak memiliki kemampuan administrasi.

### Jangan terlalu cepat membuat CDN
Mulai sederhana dan ukur.

### Jangan terlalu cepat membuat fitur sosial
Fokus pada devotional/learning experience.

### Media delivery harus terbukti
Ini adalah technical risk utama.

### Privacy anak adalah prioritas
Kumpulkan data seminimal mungkin.

---

## 46. Ringkasan Arsitektur

```text
                           GOOGLE DRIVE
                          MASTER STORAGE
                               │
                               │ Drive API
                               ▼
                       GOOGLE APPS SCRIPT
                     Scanner / Sync / Jobs
                               │
                               ▼
                           SUPABASE
                 PostgreSQL / Auth / RLS
                         /                                   /                                    ▼               ▼
                 ADMIN APP         USER APP
                 Private           Public
                    │                 │
                    │                 ▼
                    │          Video/PDF/Audio
                    │                 │
                    └─────────────────┤
                                      ▼
                              MEDIA DELIVERY
                         Drive initially / CDN later
```

---

## 47. One-Sentence Product Definition

> **Little Light adalah platform digital devotion dan pembelajaran Alkitab untuk anak Sekolah Kristen Lentera Ambarawa, dengan Google Drive sebagai master media, Supabase sebagai database/backend dan kontrol akses, Google Apps Script sebagai mesin sinkronisasi/otomasi, Admin App sebagai pusat pengelolaan konten, dan User App sebagai pemutar/pembaca yang hanya menampilkan konten yang telah disetujui dan dipublikasikan.**

---

## 48. Status Brainstorm

**CONCEPT → ARCHITECTURE DEFINED → READY FOR PROTOTYPE**

Belum production-ready sampai:
- media delivery selesai diuji;
- security selesai;
- RLS selesai;
- role selesai;
- backup selesai;
- concurrent access diuji.

---

## 49. Referensi Resmi

Google Drive API:
- https://developers.google.com/workspace/drive/api/guides/limits
- https://developers.google.com/workspace/drive/api/guides/manage-downloads
- https://developers.google.com/workspace/drive/api/guides/search-files

Google Apps Script:
- https://developers.google.com/apps-script/guides/support/troubleshooting
- https://developers.google.com/apps-script/concepts/deployments
- https://developers.google.com/apps-script/guides/v8-runtime/migration

Supabase:
- https://supabase.com/docs/guides/platform/billing-on-supabase
- https://supabase.com/docs/guides/database/overview

---

## 50. Aturan Pengembangan Selanjutnya

Jika muncul ide baru, klasifikasikan sebagai:

- `[CORE]` wajib untuk MVP
- `[IMPORTANT]` penting setelah MVP
- `[NICE TO HAVE]` tambahan
- `[FUTURE]` scale-up
- `[EXPERIMENT]` perlu POC
- `[RISK]` perlu validasi

PRIORITAS:

```text
SECURITY
   ↓
MEDIA DELIVERY
   ↓
CONTENT WORKFLOW
   ↓
USER EXPERIENCE
   ↓
AUTOMATION
   ↓
EXTRA FEATURES
```

---

## 51. Catatan Pembaruan & Implementasi (Log Teknis)

### Pembaruan 08 Oktober 2026
1. **Domain Target Ditetapkan**:
   - Domain resmi: `tbi2026-lentera.web.id`.
   - Pola routing: User App di halaman utama (`/`), Admin CMS dilindungi Supabase Auth (`/admin`).
2. **Struktur Master Google Drive**:
   - Folder Root ID: `1PDsRX77IE59SNi9Zd52heFS260OyvKzQ`.
   - Subfolder terstandardisasi:
     - `01 - RENUNGAN VIDEO` (Per bulan: 2026-07 Juli s/d 2026-10 Oktober)
     - `02 - ALKITAB LITERASI` (PAUD-TK, Fase A, Fase B, Fase C)
     - `03 - ALKITAB BERSUARA` (Perjanjian Lama, Perjanjian Baru)
     - `04 - RENUNGAN HARIAN` (Fase B, Fase C)
     - `05 - THUMBNAILS`
     - `99 - ARSIP MASTER (MOV Asli / Raw Assets)`
3. **Pipeline Video Converter (MOV -> MP4)**:
   - Tool script batch: `convert_video.bat` berbasis FFmpeg lokal di path project.
   - Konfigurasi delivery: Codec video `libx264` (CRF 22/24/26), audio `aac` 128k, flag `+faststart` (streaming-ready tanpa buffering penuh).
   - Eksekusi berhasil: 19 file video MOV periode Juli–Oktober 2026 berhasil dikonversi ke MP4 1080p & 720p tanpa mengubah/menghapus file MOV master asli.
   - Lokasi lokal: `D:\DEVIN LENTERA\TBI\Little Light\Naskah Video 2026 2027\Video Upload\converted\`.
4. **Desain Antarmuka (UI/UX) & Pemisahan Aplikasi**:
   - Resmi dipisahkan menjadi 2 aplikasi mandiri:
     - **Little Light Siswa (User App)**: `siswa-app.html` (`tbi2026-lentera.web.id`) — berorientasi anak, tanpa panel admin, salam resmi: *"Mari mulai hari ini dengan mendengarkan firman Tuhan, menonton renungan seru, dan belajar bersama Guneo, Lili, dan Joana!"*.
     - **Little Light CMS (Admin App)**: `admin-app.html` (`manage.tbi2026-lentera.web.id`) — panel kurasi guru/operator, pemicu Drive scanner, approval workflow (Draft -> Review -> Published), dan emergency unpublish.
5. **Strategi PDF Renungan Fase B & C (Keputusan Final: Opsi A - Virtual Page Range)**:
   - Dipilih **Opsi A**: File master PDF tetap 1 utuh di Google Drive tanpa dipotong secara fisik.
   - Database Supabase menggunakan tabel `devotion_ranges` untuk memetakan `start_page` dan `end_page` per minggu.
   - Viewer PDF.js di aplikasi siswa otomatis melompat ke halaman awal minggu terkait dan membatasi rentang bacaan agar siswa fokus hanya pada materi minggu berjalan.
6. **Inisialisasi Database Supabase Terpisah (Dedicated Project)**:
   - Project URL: `https://obaqikxwpektussmyjqh.supabase.co`.
   - File DDL & RLS lengkap tersimpan di `database/schema.sql` dan telah dieksekusi 100% di dashboard.
   - Mengisolasi 8 tabel: `profiles`, `media`, `devotion_ranges`, `playlists`, `playlist_items`, `daily_readings`, `audit_logs`, `sync_logs`.
   - Kebijakan RLS terverifikasi: Siswa publik anonim hanya membaca data bertanda `published = true`, seluruh hak edit & kurasi dilindungi peran `operator` / `admin`.
   - **Seeding Data Nyata Berhasil**: 18 entri media (Video renungan Juli–Oktober 2026, Alkitab Literasi 3D Claymation, Audio Kejadian 1) serta 6 entri `devotion_ranges` (Opsi A) telah terisi ke database hidup.
8. **Hasil Observasi Lengkap Struktur Google Drive & Koreksi Alkitab Bersuara**:
   - **Root Folder**: `1PDsRX77IE59SNi9Zd52heFS260OyvKzQ` (Terisi 6 folder lengkap):
     - `01 - RENUNGAN VIDEO` (`1prqKFPv6PmMOxY4lGJcrLMgepa55MKUg`): Berisi 16 file MP4 1080p renungan Guneo, Lili, Joana per subfolder bulan (Juli s.d. Oktober 2026).
     - `02 - ALKITAB LITERASI` (`16feKw5X_7M28nnGNvMyB6lxzpph95Iqb`): Berisi 12 file PDF mingguan Alkitab Literasi 3D Claymation murni kisah Alkitab (Minggu 1 s.d. 12).
     - `03 - ALKITAB BERSUARA` (`1JZGoAZ0ipy-lqJK8gCN0Qx88WTu93hrT`): Pustaka rekaman pembacaan firman Tuhan (`Pembacaan Alkitab Hari Ke-XX.mp3` untuk TK s/d Kelas 1 SD).
     - `04 - RENUNGAN HARIAN` (`1Ef_qFqC0av04XmLuOf0Dk3FeIKAKvzPF`): Berisi master PDF tahunan `Little Light TA 2026-2027.pdf` (37.5 MB, 68 halaman).
     - `05 - THUMBNAILS` (`15o42WzLTZsMfCM7OS8BlAEEhdhaNyd-w`).
     - `99 - ARSIP MASTER` (`1QXyAT8Do6nm3tv1SikOMz6tgGPDHKAD4`).
   - **Koreksi Kritis Alkitab Bersuara**:
     - Memastikan konten audio Alkitab Bersuara **bukan** audio narasi video boneka, melainkan file rekaman pembacaan firman Tuhan asli (`Pembacaan Alkitab Hari Ke-1.mp3`).
     - Pemutar audio pada `siswa-app.html` dan katalog Supabase telah diperbaiki memutar audio pembacaan Alkitab asli tersebut.
9. **Penataan Renungan Bulanan & Pengaturan Tanggal Mulai Kurikulum**:
   - **Observasi `Little Light TA 2026-2027.pdf`**: Berisi 68 halaman yang disusun berurutan per bulan (Juli 2026 s/d Juni 2027), tanpa pemisahan Fase B dan C. 52 minggu renungan telah dipetakan presisi ke halaman PDF-nya dan dimasukkan ke Supabase.
   - **UI Fokus Minggu Ini**: Tampilan awal berfokus langsung pada minggu yang sedang berjalan (Oktober 2026 • Week 1 / Hal 20) dengan selektor tab 12 bulan di bawahnya.
   - **Fitur Admin Pengaturan Tanggal Mulai**: Alkitab Literasi dan Alkitab Bersuara diatur berbasis tanggal mulai kurikulum di CMS Guru, sehingga hari aktif (Hari Ke-X) dan pekan literasi (Minggu Ke-X) terhitung otomatis secara konsisten.
10. **Kerahasiaan Dapur Sistem & Koreksi Pemetaan Video Presisi**:
   - **Indikator Rahasia**: Label "Supabase Live" dihapus total dari antarmuka publik demi kerahasiaan infrastruktur, diganti titik indikator status rahasia (Hijau = Terkoneksi, Kuning = Memuat, Merah = Offline).
   - **Akar Masalah Video "Ditegur Lewat Teman"**: Ditemukan percabangan fallback statis `else` pada prototipe awal yang mengarahkan video selain Week 2 ke file Week 1.
   - **Solusi Permanen**: Seluruh 16 file video MP4 hasil konversi telah disinkronkan ke direktori lokal, dan pemutar video menggunakan tabel pemetaan presisi `VIDEO_FILE_MAP`. Video "Ditegur Lewat Teman" kini 100% memutar file aslinya (`4_Oktober 2026_Week 3_Ditegur Lewat Teman_1080p.mp4`).
11. **Dashboard Materi Minggu Ini (Focused Weekly Learning Bundle)**:
   - Diterapkan **Dashboard Minggu Ini** tepat di bawah banner pembuka.
   - Menyajikan 4 kartu materi terkurasi khusus yang harus dibuka pada minggu berjalan:
     1. Video Renungan Minggu Ini (*Dididik Karena Disayang - Ams. 3:11-12*)
     2. Alkitab Literasi Minggu Ini (*3D Claymation Pekan Ke-2 Hari 6–10*)
     3. Alkitab Bersuara Hari Ini (*Pembacaan Alkitab Hari Ke-6*)
     4. Buku Renungan Siswa (*Holy Morning Oktober Week 1 - Halaman 20*)
   - Seluruh materi arsip bulan lampau dan katalog lengkap dipindahkan ke bagian bawah (*Jelajahi Arsip & Bulan Lainnya*) agar siswa tidak terdistraksi dan langsung tahu materi yang wajib dipelajari minggu ini.
12. **Koreksi Presisi Alkitab Literasi Minggu Ke-2 (Hari 6–10)**:
   - **Akar Masalah**: Awalnya database dan template memuat sampel uji coba dari file Minggu Ke-9 (file yang pertama kali ditemukan di folder storyboard), serta kalkulator yang mengasumsikan tanggal mulai pertengahan Juli sehingga melompat ke Minggu 9.
   - **Koreksi Nyata**: Seluruh database Supabase dan antarmuka telah dikoreksi presisi ke **Minggu Ke-2 (Hari 6–10)**. File PDF `2 Alkitab Literasi _ Minggu Ke-2 - Hari 6-10.pdf` dan rekaman audio `Pembacaan-Alkitab-Hari-Ke-6.mp3` kini menjadi materi aktif minggu ini.
13. **Perbaikan Interaktivitas Tombol Video Dashboard Minggu Ini**:
   - **Akar Masalah**: Tombol kartu video dashboard depan mengirimkan parameter `vid-2026-10-w1` (Drive File ID), sedangkan fungsi `openVideoDetail` sebelumnya hanya mencari berdasarkan `item.id` (UUID Supabase), sehingga pencarian bernilai `undefined` dan fungsi berhenti tanpa respon klik.
   - **Solusi**: Fungsi `openVideoDetail` disempurnakan untuk menerima identifikasi fleksibel (`id` UUID, `drive_file_id`, maupun kata kunci judul), disertai penambahan event klik langsung pada kotak thumbnail video.













