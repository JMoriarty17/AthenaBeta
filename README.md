# ATHENA (versi GitHub Pages)

Aplikasi web statis (PWA) untuk katalog tabel dan indikator BPS Kabupaten Barito Selatan. Tanpa server dan tanpa proses build.

## Struktur

| Folder/File | Isi |
|---|---|
| `index.html`, `tabel.html`, `strategis.html`, `panduan.html`, `backup.html` | Halaman |
| `admin.html` | Halaman admin (cek data Excel sebelum diterbitkan) |
| `data/` | `tabel.json`, `sumber.json`, `indikator.json`, `update.json` |
| `panduan/` | Isi Panduan (`index.json`, file `.md`, folder `img/`) |
| `tools/` | Skrip Python dan file Excel sumber |

Menjalankan lokal: buka terminal di folder ini, jalankan `python -m http.server`, lalu buka `http://localhost:8000`.
Deploy: unggah semua isi folder ke repo GitHub, lalu Settings > Pages > Branch `main`, folder `/ (root)`.

Data yang diperbarui langsung dipakai aplikasi saat online. Untuk perubahan halaman, CSS, atau JS, naikkan angka versi `V` di `sw.js` (misalnya `athena-v7`) supaya HP pengguna mengambil file baru.

## 1. Mengubah data tabel

Sumber: `tools/Daftar_Tabel_Update2.xlsx`, sheet pertama, kolom **Nama, Sumber, Kategori, Bab, Gambar, Link**.
- `Bab` ditulis seperti `I. GEOGRAFI DAN IKLIM` (atau hanya angka romawi).
- `Gambar` berisi link berbagi Google Drive (`.../file/d/ID/view`), file harus berstatus "siapa saja yang memiliki link". Boleh kosong.
- `Link` adalah link publikasi, satu per sumber.

Cara A (dengan halaman admin):
1. Edit Excel, buka `admin.html`, masuk dengan password.
2. Seret file Excel. Periksa ringkasan dan daftar masalah.
3. Klik **Unduh tabel.json** dan **Unduh sumber.json**.
4. Ganti kedua file di folder `data/` pada repo, lalu commit dan push.

Cara B (skrip): `pip install pandas openpyxl`, lalu `python tools/build_data.py`, lalu commit folder `data/`.

**Update terakhir (Backup Publikasi)**: edit `data/update.json` langsung, atau lewat `admin.html` (tambah/hapus, lalu **Unduh update.json** dan ganti filenya). Entri paling atas tampil sebagai "Rilis terbaru" di Beranda.

**Ganti password admin**: jalankan `python -c "import hashlib;print(hashlib.sha256(b'PASSWORDBARU').hexdigest())"`, lalu tempel hasilnya ke `HASH` di `admin.html`. Catatan: password ini hanya penghalang tampilan, bukan pengaman data.

## 2. Mengubah data Indikator Strategis

Sumber: `tools/Indikator_Strategis.xlsx`.
- **Sheet data** (`KP_Penduduk`, `KM`, `IPM`, `PDRB`, dst.): kolom pertama adalah sumbu X (tahun atau kategori), kolom lain adalah angka. Tambah tahun baru dengan menambah baris.
- **Sheet `Kelompok`**: `id`, `nama`, dan `gambar` (link Drive untuk cover kartu).
- **Sheet `Meta`**: satu baris = satu grafik.

| Kolom Meta | Arti |
|---|---|
| `kelompok` | id kelompok (harus ada di sheet `Kelompok`) |
| `judul` | judul grafik |
| `sheet` | nama sheet data |
| `tipe` | `line` (garis), `bar` (batang), `hbar` (batang mendatar, diurutkan terbesar), `pyramid` (piramida; 2 kolom: laki-laki, perempuan) |
| `kolom` | nama kolom yang digambar, pisahkan dengan koma untuk beberapa seri |
| `satuan` | satuan yang ditampilkan |
| `kpi` | `1` agar nilai terbaru tampil sebagai angka kunci (kolom pertama) |
| `catatan` | catatan kecil di bawah judul (boleh kosong) |

Setelah mengedit: `python tools/build_indikator.py`, lalu commit `data/indikator.json`.
Tahun tabel Angkatan Kerja dan satuan PPK masih perlu dikonfirmasi (lihat kolom `catatan`).

## 3. Mengisi konten Panduan

- Daftar kategori ada di `panduan/index.json`: `id`, `judul`, `desk`, dan `file`. Tambah kategori = tambah satu entri dan satu file `.md`.
- Tiap file `.md` diawali tanggal pembaruan:

```
<!-- diperbarui: 2026-11-11 -->
## Judul bagian
Paragraf biasa, **tebal**, *miring*, dan [tautan](https://contoh.id).

| No | Nama | Senin |
|---|---|---|
| 1 | Contoh | 8.00-12.00 |

![QR Buku Tamu](img/qr-buku-tamu.webp)
```

- Gambar: taruh di `panduan/img/` (format WebP atau PNG yang sudah dikecilkan), lalu rujuk dengan `img/nama-file.webp`. Gambar bisa diketuk untuk diperbesar.
- Tabel dibuat dengan format di atas dan otomatis bisa digeser ke samping di HP.
- Bisa diedit langsung di GitHub (ikon pensil pada file), lalu **Commit changes**.

## Tema

Tombol di pojok kanan header berganti antara **Otomatis** (mengikuti HP), **Terang**, dan **Gelap**. Pilihan tersimpan di perangkat.

## Jika halaman tidak muncul di GitHub Pages

1. Tunggu 1-2 menit setelah commit, lalu muat ulang paksa (atau hapus data situs di pengaturan browser, karena aplikasi menyimpan cache).
2. Buka langsung `https://USERNAME.github.io/REPO/panduan/index.json` dan salah satu file `.md` di browser. Kalau muncul 404, filenya belum terunggah atau salah folder.
3. Pastikan file kosong bernama `.nojekyll` ada di folder paling atas repo. Tanpa file ini GitHub memproses file `.md` dan mengubahnya menjadi HTML, sehingga file aslinya tidak bisa dibaca aplikasi. Kalau file berawalan titik tidak ikut terunggah, buat lewat Add file > Create new file, beri nama `.nojekyll`.
4. Nama folder dan file peka huruf besar-kecil (`panduan/`, bukan `Panduan/`).
