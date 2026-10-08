-- ==============================================================================
-- LITTLE LIGHT — SEKOLAH KRISTEN LENTERA AMBARAWA
-- DATABASE SCHEMA (SUPABASE POSTGRESQL)
-- Domain Target: tbi2026-lentera.web.id
-- Master Storage: Google Drive (1PDsRX77IE59SNi9Zd52heFS260OyvKzQ)
-- ==============================================================================

-- 0. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. PROFILES (ROLE: OPERATOR / ADMIN)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT NOT NULL CHECK (role IN ('operator', 'admin')) DEFAULT 'operator',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. MEDIA (KATALOG MASTER FILE DRIVE)
CREATE TABLE IF NOT EXISTS public.media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    drive_file_id TEXT UNIQUE NOT NULL,
    drive_url TEXT NOT NULL,
    direct_stream_url TEXT,
    title TEXT NOT NULL,
    description TEXT,
    media_type TEXT NOT NULL CHECK (media_type IN ('video', 'pdf', 'audio', 'thumbnail')),
    mime_type TEXT,
    file_size BIGINT,
    duration TEXT,
    date DATE,
    week_number INT,
    phase TEXT CHECK (phase IN ('paud_tk', 'fase_a', 'fase_b', 'fase_c', 'semua')),
    thumbnail_url TEXT,
    storage_provider TEXT NOT NULL DEFAULT 'google_drive',
    status TEXT NOT NULL CHECK (status IN ('draft', 'review', 'approved', 'published', 'archived', 'rejected')) DEFAULT 'draft',
    published BOOLEAN NOT NULL DEFAULT FALSE,
    published_at TIMESTAMPTZ,
    created_by UUID REFERENCES auth.users(id),
    approved_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexing untuk query cepat aplikasi siswa
CREATE INDEX IF NOT EXISTS idx_media_published ON public.media (published, media_type, date);
CREATE INDEX IF NOT EXISTS idx_media_drive_id ON public.media (drive_file_id);

-- 3. DEVOTION RANGES (OPSI A: VIRTUAL PAGE RANGE UNTUK 1 MASTER PDF TAHUNAN FASE B & C)
CREATE TABLE IF NOT EXISTS public.devotion_ranges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    media_id UUID REFERENCES public.media(id) ON DELETE CASCADE,
    phase TEXT NOT NULL CHECK (phase IN ('fase_b', 'fase_c')),
    week_number INT NOT NULL,
    start_page INT NOT NULL,
    end_page INT NOT NULL,
    title TEXT NOT NULL,
    bible_verse TEXT,
    theme TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_page_range CHECK (start_page <= end_page)
);

CREATE INDEX IF NOT EXISTS idx_devotion_phase_week ON public.devotion_ranges (phase, week_number);

-- 4. PLAYLISTS
CREATE TABLE IF NOT EXISTS public.playlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    thumbnail_url TEXT,
    status TEXT NOT NULL DEFAULT 'published',
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. PLAYLIST ITEMS
CREATE TABLE IF NOT EXISTS public.playlist_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    playlist_id UUID NOT NULL REFERENCES public.playlists(id) ON DELETE CASCADE,
    media_id UUID NOT NULL REFERENCES public.media(id) ON DELETE CASCADE,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (playlist_id, media_id)
);

CREATE INDEX IF NOT EXISTS idx_playlist_items_order ON public.playlist_items (playlist_id, sort_order);

-- 6. DAILY READINGS (MESIN KONTEN HARIAN "HARI INI")
CREATE TABLE IF NOT EXISTS public.daily_readings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE UNIQUE NOT NULL,
    bible_reference TEXT NOT NULL,
    video_media_id UUID REFERENCES public.media(id) ON DELETE SET NULL,
    pdf_literasi_id UUID REFERENCES public.media(id) ON DELETE SET NULL,
    audio_media_id UUID REFERENCES public.media(id) ON DELETE SET NULL,
    devotion_range_b_id UUID REFERENCES public.devotion_ranges(id) ON DELETE SET NULL,
    devotion_range_c_id UUID REFERENCES public.devotion_ranges(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_daily_readings_date ON public.daily_readings (date);

-- 7. AUDIT LOGS (RIWAYAT TINDAKAN CMS GURU & OPERATOR)
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_id UUID REFERENCES auth.users(id),
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    before_data JSONB,
    after_data JSONB,
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. SYNC LOGS (LOG SCANNER GOOGLE APPS SCRIPT)
CREATE TABLE IF NOT EXISTS public.sync_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    files_scanned INT DEFAULT 0,
    files_added INT DEFAULT 0,
    files_updated INT DEFAULT 0,
    errors INT DEFAULT 0,
    status TEXT DEFAULT 'success',
    error_message TEXT
);

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================

-- Aktifkan RLS di semua tabel
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.media ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.devotion_ranges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.playlists ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.playlist_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.daily_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sync_logs ENABLE ROW LEVEL SECURITY;

-- Helper Function: Mengecek apakah pengguna login adalah admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND role = 'admin' AND active = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Helper Function: Mengecek apakah pengguna login adalah staf (operator/admin)
CREATE OR REPLACE FUNCTION public.is_staff()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND active = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ------------------------------------------------------------------------------
-- A. KEBIJAKAN MEDIA
-- ------------------------------------------------------------------------------
-- 1. Siswa (Anonim / Publik): Hanya bisa membaca konten yang 'published = true'
CREATE POLICY "Public Read Published Media" ON public.media
    FOR SELECT USING (published = TRUE);

-- 2. Staf (Operator & Admin): Bisa melihat semua status (draft, review, dll)
CREATE POLICY "Staff Full Select Media" ON public.media
    FOR SELECT TO authenticated USING (public.is_staff());

-- 3. Staf: Bisa menambahkan media baru dari Drive scan
CREATE POLICY "Staff Insert Media" ON public.media
    FOR INSERT TO authenticated WITH CHECK (public.is_staff());

-- 4. Staf: Bisa mengedit metadata
CREATE POLICY "Staff Update Media" ON public.media
    FOR UPDATE TO authenticated USING (public.is_staff());

-- 5. Admin: Bisa menghapus media
CREATE POLICY "Admin Delete Media" ON public.media
    FOR DELETE TO authenticated USING (public.is_admin());

-- ------------------------------------------------------------------------------
-- B. KEBIJAKAN DEVOTION RANGES & PLAYLIST & DAILY READINGS
-- ------------------------------------------------------------------------------
-- Publik bisa membaca
CREATE POLICY "Public Read Devotion Ranges" ON public.devotion_ranges FOR SELECT USING (TRUE);
CREATE POLICY "Public Read Playlists" ON public.playlists FOR SELECT USING (status = 'published');
CREATE POLICY "Public Read Playlist Items" ON public.playlist_items FOR SELECT USING (TRUE);
CREATE POLICY "Public Read Daily Readings" ON public.daily_readings FOR SELECT USING (TRUE);

-- Staf bisa mengelola
CREATE POLICY "Staff Manage Devotion Ranges" ON public.devotion_ranges FOR ALL TO authenticated USING (public.is_staff());
CREATE POLICY "Staff Manage Playlists" ON public.playlists FOR ALL TO authenticated USING (public.is_staff());
CREATE POLICY "Staff Manage Playlist Items" ON public.playlist_items FOR ALL TO authenticated USING (public.is_staff());
CREATE POLICY "Staff Manage Daily Readings" ON public.daily_readings FOR ALL TO authenticated USING (public.is_staff());

-- ------------------------------------------------------------------------------
-- C. KEBIJAKAN PROFILES & AUDIT LOGS
-- ------------------------------------------------------------------------------
CREATE POLICY "Staff Read Profiles" ON public.profiles FOR SELECT TO authenticated USING (public.is_staff());
CREATE POLICY "Admin Manage Profiles" ON public.profiles FOR ALL TO authenticated USING (public.is_admin());
CREATE POLICY "Staff Insert Audit Logs" ON public.audit_logs FOR INSERT TO authenticated WITH CHECK (public.is_staff());
CREATE POLICY "Admin Read Audit Logs" ON public.audit_logs FOR SELECT TO authenticated USING (public.is_admin());
CREATE POLICY "Staff Manage Sync Logs" ON public.sync_logs FOR ALL TO authenticated USING (public.is_staff());

-- ------------------------------------------------------------------------------
-- TRIGGER AUTO-UPDATE `updated_at`
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_media_modtime BEFORE UPDATE ON public.media FOR EACH ROW EXECUTE PROCEDURE public.handle_updated_at();
CREATE TRIGGER update_devotion_ranges_modtime BEFORE UPDATE ON public.devotion_ranges FOR EACH ROW EXECUTE PROCEDURE public.handle_updated_at();
CREATE TRIGGER update_daily_readings_modtime BEFORE UPDATE ON public.daily_readings FOR EACH ROW EXECUTE PROCEDURE public.handle_updated_at();
