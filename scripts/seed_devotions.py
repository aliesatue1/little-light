import urllib.request
import json

SUPABASE_URL = 'https://obaqikxwpektussmyjqh.supabase.co'
SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iYXFpa3h3cGVrdHVzc215anFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MTQwMzA3OSwiZXhwIjoyMTA2OTc5MDc5fQ.YvSqaqUk_IA90vkvlqV80cWdYOqNJ9eOdFeuyDhyP_U'

# Get or create master pdf media_id
master_pdf = {
    'drive_file_id': 'pdf-master-fase-bc-2026',
    'drive_url': 'https://drive.google.com/file/d/1Kt0Zre-xT2YJaGd7rGDkrah-jcTvTDf5/view?usp=drive_link',
    'title': 'Little Light TA 2026-2027 (Master PDF)',
    'description': 'Master buku renungan tahunan kelas 3-6 SD Lentera Ambarawa',
    'media_type': 'pdf',
    'mime_type': 'application/pdf',
    'phase': 'semua',
    'status': 'published',
    'published': True,
    'storage_provider': 'google_drive'
}

req_m = urllib.request.Request(
    f'{SUPABASE_URL}/rest/v1/media?on_conflict=drive_file_id',
    data=json.dumps([master_pdf]).encode('utf-8'),
    headers={
        'apikey': SERVICE_KEY,
        'Authorization': f'Bearer {SERVICE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates,return=representation'
    },
    method='POST'
)
with urllib.request.urlopen(req_m) as resp:
    m_data = json.loads(resp.read().decode())
    media_id = m_data[0]['id']

# Clean up old devotion ranges
req_del = urllib.request.Request(
    f'{SUPABASE_URL}/rest/v1/devotion_ranges?media_id=eq.{media_id}',
    headers={'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'},
    method='DELETE'
)
try:
    urllib.request.urlopen(req_del)
except:
    pass

# All 52 weeks mapped across all 12 months (no separation of Phase B vs Phase C!)
schedule = [
    # JULI 2026
    {'month': 'Juli 2026', 'theme': 'Holy Thought for God', 'week': 1, 'page': 4, 'verse': 'Phil. 4:8'},
    {'month': 'Juli 2026', 'theme': 'Holy Thought for God', 'week': 2, 'page': 5, 'verse': 'Phil. 4:8'},
    {'month': 'Juli 2026', 'theme': 'Holy Thought for God', 'week': 3, 'page': 6, 'verse': 'Phil. 4:8'},
    {'month': 'Juli 2026', 'theme': 'Holy Thought for God', 'week': 4, 'page': 7, 'verse': 'Phil. 4:8'},
    # AGUSTUS 2026
    {'month': 'Agustus 2026', 'theme': 'Encounter Changed Life', 'week': 1, 'page': 9, 'verse': 'Luk. 19:8-9'},
    {'month': 'Agustus 2026', 'theme': 'Encounter Changed Life', 'week': 2, 'page': 10, 'verse': 'Luk. 19:8-9'},
    {'month': 'Agustus 2026', 'theme': 'Encounter Changed Life', 'week': 3, 'page': 11, 'verse': 'Luk. 19:8-9'},
    {'month': 'Agustus 2026', 'theme': 'Encounter Changed Life', 'week': 4, 'page': 12, 'verse': 'Luk. 19:8-9'},
    {'month': 'Agustus 2026', 'theme': 'Encounter Changed Life', 'week': 5, 'page': 13, 'verse': 'Luk. 19:8-9'},
    # SEPTEMBER 2026
    {'month': 'September 2026', 'theme': 'Attentiveness for God’s Word', 'week': 1, 'page': 15, 'verse': 'Mat. 13:1-16'},
    {'month': 'September 2026', 'theme': 'Attentiveness for God’s Word', 'week': 2, 'page': 16, 'verse': 'Mat. 13:1-16'},
    {'month': 'September 2026', 'theme': 'Attentiveness for God’s Word', 'week': 3, 'page': 17, 'verse': 'Mat. 13:1-16'},
    {'month': 'September 2026', 'theme': 'Attentiveness for God’s Word', 'week': 4, 'page': 18, 'verse': 'Mat. 13:1-16'},
    # OKTOBER 2026
    {'month': 'Oktober 2026', 'theme': 'Determined to be taught by God', 'week': 1, 'page': 20, 'verse': 'Ams. 3:11-12'},
    {'month': 'Oktober 2026', 'theme': 'Determined to be taught by God', 'week': 2, 'page': 21, 'verse': 'Ams. 3:11-12'},
    {'month': 'Oktober 2026', 'theme': 'Determined to be taught by God', 'week': 3, 'page': 22, 'verse': 'Ams. 3:11-12'},
    {'month': 'Oktober 2026', 'theme': 'Determined to be taught by God', 'week': 4, 'page': 23, 'verse': 'Ams. 3:11-12'},
    # NOVEMBER 2026
    {'month': 'November 2026', 'theme': 'Heart with Diligence', 'week': 1, 'page': 25, 'verse': 'Prov. 4:23'},
    {'month': 'November 2026', 'theme': 'Heart with Diligence', 'week': 2, 'page': 26, 'verse': 'Prov. 4:23'},
    {'month': 'November 2026', 'theme': 'Heart with Diligence', 'week': 3, 'page': 27, 'verse': 'Prov. 4:23'},
    {'month': 'November 2026', 'theme': 'Heart with Diligence', 'week': 4, 'page': 28, 'verse': 'Prov. 4:23'},
    {'month': 'November 2026', 'theme': 'Heart with Diligence', 'week': 5, 'page': 29, 'verse': 'Prov. 4:23'},
    # DESEMBER 2026
    {'month': 'Desember 2026', 'theme': 'Beauty of the Inner Heart', 'week': 1, 'page': 31, 'verse': '1 Sam. 16:7'},
    {'month': 'Desember 2026', 'theme': 'Beauty of the Inner Heart', 'week': 2, 'page': 32, 'verse': '1 Sam. 16:7'},
    {'month': 'Desember 2026', 'theme': 'Beauty of the Inner Heart', 'week': 3, 'page': 33, 'verse': '1 Sam. 16:7'},
    {'month': 'Desember 2026', 'theme': 'Beauty of the Inner Heart', 'week': 4, 'page': 34, 'verse': '1 Sam. 16:7'},
    # JANUARI 2027
    {'month': 'Januari 2027', 'theme': 'Repentance Rooted in the Word', 'week': 1, 'page': 36, 'verse': 'Yoh. 12:44-50'},
    {'month': 'Januari 2027', 'theme': 'Repentance Rooted in the Word', 'week': 2, 'page': 37, 'verse': 'Yoh. 12:44-50'},
    {'month': 'Januari 2027', 'theme': 'Repentance Rooted in the Word', 'week': 3, 'page': 38, 'verse': 'Yoh. 12:44-50'},
    {'month': 'Januari 2027', 'theme': 'Repentance Rooted in the Word', 'week': 4, 'page': 39, 'verse': 'Yoh. 12:44-50'},
    # FEBRUARI 2027
    {'month': 'Februari 2027', 'theme': 'Touched Heart Changing Life', 'week': 1, 'page': 41, 'verse': 'Tit. 3:5; Ams. 23:12'},
    {'month': 'Februari 2027', 'theme': 'Touched Heart Changing Life', 'week': 2, 'page': 42, 'verse': 'Tit. 3:5; Ams. 23:12'},
    {'month': 'Februari 2027', 'theme': 'Touched Heart Changing Life', 'week': 3, 'page': 43, 'verse': 'Tit. 3:5; Ams. 23:12'},
    {'month': 'Februari 2027', 'theme': 'Touched Heart Changing Life', 'week': 4, 'page': 44, 'verse': 'Tit. 3:5; Ams. 23:12'},
    # MARET 2027
    {'month': 'Maret 2027', 'theme': 'Hidup yang Dipersembahkan', 'week': 1, 'page': 46, 'verse': 'Kol. 3:23'},
    {'month': 'Maret 2027', 'theme': 'Hidup yang Dipersembahkan', 'week': 2, 'page': 47, 'verse': 'Kol. 3:23'},
    {'month': 'Maret 2027', 'theme': 'Hidup yang Dipersembahkan', 'week': 3, 'page': 48, 'verse': 'Kol. 3:23'},
    {'month': 'Maret 2027', 'theme': 'Hidup yang Dipersembahkan', 'week': 4, 'page': 49, 'verse': 'Kol. 3:23'},
    {'month': 'Maret 2027', 'theme': 'Hidup yang Dipersembahkan', 'week': 5, 'page': 50, 'verse': 'Kol. 3:23'},
    # APRIL 2027
    {'month': 'April 2027', 'theme': 'An Extraordinary Life of Jesus', 'week': 1, 'page': 52, 'verse': 'Kej. 12:1-9'},
    {'month': 'April 2027', 'theme': 'An Extraordinary Life of Jesus', 'week': 2, 'page': 53, 'verse': 'Kej. 12:1-9'},
    {'month': 'April 2027', 'theme': 'An Extraordinary Life of Jesus', 'week': 3, 'page': 54, 'verse': 'Kej. 12:1-9'},
    {'month': 'April 2027', 'theme': 'An Extraordinary Life of Jesus', 'week': 4, 'page': 55, 'verse': 'Kej. 12:1-9'},
    # MEI 2027
    {'month': 'Mei 2027', 'theme': 'Nurturing the Lost for God', 'week': 1, 'page': 57, 'verse': 'Mat. 28:19-20'},
    {'month': 'Mei 2027', 'theme': 'Nurturing the Lost for God', 'week': 2, 'page': 58, 'verse': 'Mat. 28:19-20'},
    {'month': 'Mei 2027', 'theme': 'Nurturing the Lost for God', 'week': 3, 'page': 59, 'verse': 'Mat. 28:19-20'},
    {'month': 'Mei 2027', 'theme': 'Nurturing the Lost for God', 'week': 4, 'page': 60, 'verse': 'Mat. 28:19-20'},
    {'month': 'Mei 2027', 'theme': 'Nurturing the Lost for God', 'week': 5, 'page': 61, 'verse': 'Mat. 28:19-20'},
    # JUNI 2027
    {'month': 'Juni 2027', 'theme': 'Docility to Walk with God', 'week': 1, 'page': 63, 'verse': 'Maz. 86:11'},
    {'month': 'Juni 2027', 'theme': 'Docility to Walk with God', 'week': 2, 'page': 64, 'verse': 'Maz. 86:11'},
    {'month': 'Juni 2027', 'theme': 'Docility to Walk with God', 'week': 3, 'page': 65, 'verse': 'Maz. 86:11'},
    {'month': 'Juni 2027', 'theme': 'Docility to Walk with God', 'week': 4, 'page': 66, 'verse': 'Maz. 86:11'}
]

rows = []
for item in schedule:
    rows.append({
        'media_id': media_id,
        'phase': 'fase_b', # keep check constraint satisfied
        'week_number': item['week'],
        'start_page': item['page'],
        'end_page': item['page'],
        'title': f"{item['month']} • Week {item['week']}",
        'bible_verse': item['verse'],
        'theme': item['theme']
    })

req_ins = urllib.request.Request(
    f'{SUPABASE_URL}/rest/v1/devotion_ranges',
    data=json.dumps(rows).encode('utf-8'),
    headers={
        'apikey': SERVICE_KEY,
        'Authorization': f'Bearer {SERVICE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    },
    method='POST'
)

with urllib.request.urlopen(req_ins) as resp:
    res = json.loads(resp.read().decode())
    print(f'SUCCESS! Seeded {len(res)} weeks across all 12 months into Supabase devotion_ranges!')
