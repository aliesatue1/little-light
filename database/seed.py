import urllib.request
import json

SUPABASE_URL = 'https://obaqikxwpektussmyjqh.supabase.co'
SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iYXFpa3h3cGVrdHVzc215anFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MTQwMzA3OSwiZXhwIjoyMTA2OTc5MDc5fQ.YvSqaqUk_IA90vkvlqV80cWdYOqNJ9eOdFeuyDhyP_U'

real_media = [
    # OKTOBER 2026
    {
        'drive_file_id': 'vid-2026-10-w1',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Dididik Karena Disayang',
        'description': 'Amsal 3:11-12. Robot mainan Guneo disita Ms Guru karena dilempar dekat jendela kaca. Joana & Lili mengingatkannya bahwa teguran guru dan orang tua adalah bukti kasih sayang Tuhan agar kita aman dan berkarakter baik.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:42',
        'date': '2026-10-08',
        'week_number': 1,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-10-w2',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Jangan Pura-Pura Ngga Dengar',
        'description': 'Mazmur 95:7-8. Guneo asyik main bola saat mendung dan pura-pura tidak dengar panggilan Ms Guru. Lili dan Joana mengingatkan firman Tuhan agar hati tidak keras dan langsung taat.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '06:15',
        'date': '2026-10-15',
        'week_number': 2,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-10-w3',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Ditegur Lewat Teman',
        'description': '2 Samuel 12:1-13. Guneo mengambil penghapus stroberi milik Lili. Joana menegurnya dengan perumpamaan seperti Nabi Natan menegur Raja Daud sehingga Guneo sadar dan mengembalikan barang temannya.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:30',
        'date': '2026-10-22',
        'week_number': 3,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    # SEPTEMBER 2026
    {
        'drive_file_id': 'vid-2026-09-w1',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Hatiku Tanah yang Subur',
        'description': 'Renungan anak seri September Week 1: Belajar menjaga hati agar menjadi tanah yang subur bagi benih firman Tuhan.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:20',
        'date': '2026-09-03',
        'week_number': 1,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-09-w2',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Nasihat Itu Tanda Sayang',
        'description': 'Renungan anak seri September Week 2: Menghargai nasihat yang diberikan demi kebaikan masa depan kita.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:40',
        'date': '2026-09-10',
        'week_number': 2,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-09-w3',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Buku Petunjuk Hebat',
        'description': 'Renungan anak seri September Week 3: Alkitab adalah buku petunjuk kehidupan terbaik yang menuntun langkah kita.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:35',
        'date': '2026-09-17',
        'week_number': 3,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-09-w4',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Jangan Cuma Hafal, Ayo Lakukan!',
        'description': 'Renungan anak seri September Week 4: Menjadi pelaku firman dan bukan hanya pendengar atau penghafal semata.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '06:00',
        'date': '2026-09-24',
        'week_number': 4,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    # AGUSTUS 2026
    {
        'drive_file_id': 'vid-2026-08-w1',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Tak Pernah Sama Lagi',
        'description': 'Renungan anak seri Agustus Week 1: Mengalami perubahan hidup bersama kasih Kristus.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:10',
        'date': '2026-08-06',
        'week_number': 1,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-08-w2',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Hati yang Segar Kembali',
        'description': 'Renungan anak seri Agustus Week 2: Sukacita dan damai sejahtera yang menyegarkan jiwa.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:25',
        'date': '2026-08-13',
        'week_number': 2,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-08-w3',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Jadi Anak yang Baru',
        'description': 'Renungan anak seri Agustus Week 3: Menanggalkan kebiasaan lama dan menjadi ciptaan yang baru.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:15',
        'date': '2026-08-20',
        'week_number': 3,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-08-w4',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Berani Beda Nggak Ikut-ikutan',
        'description': 'Renungan anak seri Agustus Week 4: Memiliki keberanian untuk berpegang pada kebenaran walau teman lain tidak setuju.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:30',
        'date': '2026-08-27',
        'week_number': 4,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-08-w5',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Senter Kehidupan',
        'description': 'Renungan anak seri Agustus Week 5: Firman-Mu pelita bagi kakiku dan terang bagi jalanku.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:45',
        'date': '2026-08-31',
        'week_number': 5,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    # JULI 2026
    {
        'drive_file_id': 'vid-2026-07-w1',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Mengapa Harus Memikirkan Apa yang Baik',
        'description': 'Filipi 4:8. Renungan anak seri Juli Week 1: Mengisi pikiran dengan hal-hal yang manis, benar, dan sedap didengar.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:10',
        'date': '2026-07-09',
        'week_number': 1,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-07-w2',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Hati yang Keras Seperti Batu',
        'description': 'Renungan anak seri Juli Week 2: Melembutkan hati di hadapan Tuhan dan sesama.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:30',
        'date': '2026-07-16',
        'week_number': 2,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-07-w3',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Minta Maaf yang Sungguh-Sungguh',
        'description': 'Renungan anak seri Juli Week 3: Keberanian untuk mengakui kesalahan dan meminta maaf dengan tulus.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:20',
        'date': '2026-07-23',
        'week_number': 3,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    {
        'drive_file_id': 'vid-2026-07-w4',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Berani Jujur Walau Sendirian',
        'description': 'Renungan anak seri Juli Week 4: Berdiri teguh dalam kejujuran di setiap keadaan.',
        'media_type': 'video',
        'mime_type': 'video/mp4',
        'duration': '05:40',
        'date': '2026-07-30',
        'week_number': 4,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    # ALKITAB LITERASI 3D CLAYMATION
    {
        'drive_file_id': 'pdf-literasi-m9',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Alkitab Literasi Minggu Ke-9 (Hari 41-45)',
        'description': 'Kisah Tuhan Yesus Memberkati Anak-anak. Format 3D Claymation Open Book Spread: kiri seni tanah liat 3D murni adegan Alkitab, kanan kertas gading teks firman Tuhan anak PAUD/TK.',
        'media_type': 'pdf',
        'mime_type': 'application/pdf',
        'duration': '5 Hari Bacaan',
        'date': '2026-10-08',
        'week_number': 9,
        'phase': 'paud_tk',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    },
    # ALKITAB BERSUARA
    {
        'drive_file_id': 'audio-kejadian-01',
        'drive_url': 'https://drive.google.com/drive/folders/1PDsRX77IE59SNi9Zd52heFS260OyvKzQ',
        'title': 'Kejadian 1 — Penciptaan Langit & Bumi',
        'description': 'Audio Alkitab dramatisasi dengan iringan musik untuk renungan pendengaran anak sekolah Minggu & PAUD/SD Lentera.',
        'media_type': 'audio',
        'mime_type': 'audio/mpeg',
        'duration': '08:12',
        'date': '2026-10-08',
        'week_number': 1,
        'phase': 'semua',
        'status': 'published',
        'published': True,
        'storage_provider': 'google_drive'
    }
]

# Insert or upsert via Supabase REST API
req = urllib.request.Request(
    f'{SUPABASE_URL}/rest/v1/media?on_conflict=drive_file_id',
    data=json.dumps(real_media).encode('utf-8'),
    headers={
        'apikey': SERVICE_KEY,
        'Authorization': f'Bearer {SERVICE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates,return=representation'
    },
    method='POST'
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print(f'SEEDED SUCCESSFULLY! Total {len(res)} live items inserted/updated in Supabase media table!')
