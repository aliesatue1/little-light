/**
 * LITTLE LIGHT — GOOGLE APPS SCRIPT DRIVE SCANNER & SUPABASE SYNC
 * Sekolah Kristen Lentera Ambarawa
 * Domain: tbi2026-lentera.web.id
 */

const CONFIG = {
  SUPABASE_URL: "https://obaqikxwpektussmyjqh.supabase.co",
  SUPABASE_SERVICE_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9iYXFpa3h3cGVrdHVzc215anFoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MTQwMzA3OSwiZXhwIjoyMTA2OTc5MDc5fQ.YvSqaqUk_IA90vkvlqV80cWdYOqNJ9eOdFeuyDhyP_U",
  ROOT_FOLDER_ID: "1PDsRX77IE59SNi9Zd52heFS260OyvKzQ"
};

/**
 * Pemicu Utama: Scan Google Drive & Kirim ke Supabase
 */
function scanAndSyncDrive() {
  Logger.log("=== MULAI SCAN GOOGLE DRIVE LITTLE LIGHT ===");
  const root = DriveApp.getFolderById(CONFIG.ROOT_FOLDER_ID);
  
  let scannedCount = 0;
  let addedCount = 0;
  
  // 1. Scan Folder 01 - RENUNGAN VIDEO
  const videoFolders = root.getFoldersByName("01 - RENUNGAN VIDEO");
  if (videoFolders.hasNext()) {
    const videoRoot = videoFolders.next();
    const subMonth = videoRoot.getFolders();
    while (subMonth.hasNext()) {
      const monthFolder = subMonth.next();
      const files = monthFolder.getFiles();
      while (files.hasNext()) {
        const file = files.next();
        scannedCount++;
        if (file.getMimeType().includes("video") || file.getName().endsWith(".mp4")) {
          syncFileToSupabase(file, "video", monthFolder.getName());
          addedCount++;
        }
      }
    }
  }

  // 2. Scan Folder 02 - ALKITAB LITERASI
  const literasiFolders = root.getFoldersByName("02 - ALKITAB LITERASI");
  if (literasiFolders.hasNext()) {
    const litRoot = literasiFolders.next();
    const files = litRoot.getFiles();
    while (files.hasNext()) {
      const file = files.next();
      scannedCount++;
      if (file.getMimeType().includes("pdf") || file.getName().endsWith(".pdf")) {
        syncFileToSupabase(file, "pdf", "paud_tk");
        addedCount++;
      }
    }
  }

  Logger.log(`=== SCAN SELESAI: ${scannedCount} file terbaca, ${addedCount} disinkronkan ke Supabase ===`);
}

/**
 * Mengirim metadata file ke Supabase REST API
 */
function syncFileToSupabase(file, mediaType, folderContext) {
  const fileId = file.getId();
  const name = file.getName();
  const size = file.getSize();
  const mimeType = file.getMimeType();
  const url = file.getUrl();

  // Parsing Nama File
  const parsed = parseFileName(name, mediaType);

  const payload = {
    drive_file_id: fileId,
    drive_url: url,
    title: parsed.title || name,
    description: parsed.description || `File materi ${mediaType} Little Light`,
    media_type: mediaType,
    mime_type: mimeType,
    file_size: size,
    week_number: parsed.week_number || null,
    phase: parsed.phase || "semua",
    storage_provider: "google_drive",
    status: "published",
    published: true
  };

  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "apikey": CONFIG.SUPABASE_SERVICE_KEY,
      "Authorization": "Bearer " + CONFIG.SUPABASE_SERVICE_KEY,
      "Prefer": "resolution=merge-duplicates"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(CONFIG.SUPABASE_URL + "/rest/v1/media?on_conflict=drive_file_id", options);
  Logger.log(`Sync [${name}]: HTTP ${response.getResponseCode()}`);
}

/**
 * Parser Nama File Standar Lentera
 */
function parseFileName(name, type) {
  let title = name.replace(/\.[^/.]+$/, "").replace(/_\d+p$/, "");
  let week_number = null;
  let phase = "semua";

  const weekMatch = name.match(/Week[ _](\d+)/i);
  if (weekMatch) {
    week_number = parseInt(weekMatch[1]);
  }

  // Pisahkan judul jika ada format prefix
  const parts = title.split("_");
  if (parts.length >= 3) {
    title = parts.slice(2).join("_").trim();
  }

  return { title, week_number, phase };
}
