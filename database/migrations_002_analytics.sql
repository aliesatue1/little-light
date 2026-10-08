-- ==============================================================================
-- LITTLE LIGHT — TABEL ANALITIK KONTEN (MEDIA ANALYTICS)
-- Jalankan skrip ini di SQL Editor Supabase untuk mengaktifkan pelacakan analitik
-- ==============================================================================

CREATE TABLE IF NOT EXISTS public.media_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    media_id UUID REFERENCES public.media(id) ON DELETE SET NULL,
    content_title TEXT NOT NULL,
    media_type TEXT NOT NULL CHECK (media_type IN ('video', 'pdf', 'audio', 'renungan')),
    device_type TEXT NOT NULL, -- 'Mobile (Android)', 'Mobile (iOS)', 'Desktop (Windows)', 'Desktop (Mac)', 'Lainnya'
    browser TEXT NOT NULL, -- 'Chrome', 'Lemur Browser', 'Safari', 'Edge', 'Firefox', 'Lainnya'
    view_type TEXT DEFAULT 'play', -- 'play', 'read', 'open'
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analytics_media ON public.media_analytics (media_id, media_type, created_at);
CREATE INDEX IF NOT EXISTS idx_analytics_device ON public.media_analytics (device_type, browser);

ALTER TABLE public.media_analytics ENABLE ROW LEVEL SECURITY;

-- Izinkan siswa publik memasukkan log aktivitas (play / read)
DROP POLICY IF EXISTS "Public Insert Media Analytics" ON public.media_analytics;
CREATE POLICY "Public Insert Media Analytics" ON public.media_analytics 
    FOR INSERT WITH CHECK (TRUE);

-- Izinkan staf membaca seluruh data analitik
DROP POLICY IF EXISTS "Staff Read Media Analytics" ON public.media_analytics;
CREATE POLICY "Staff Read Media Analytics" ON public.media_analytics 
    FOR SELECT USING (TRUE);
