# PinangSort 

Aplikasi web (PWA) untuk mendeteksi dan mengklasifikasikan mutu biji pinang (Grade A / Grade B / Jelek) menggunakan computer vision.

## Tech Stack

### Frontend
- **React** (via Vite)
- **Tailwind CSS** -> styling
- **vite-plugin-pwa** -> PWA support (installable, offline-capable)
- **React Router** -> routing
- **fetch / axios** -> komunikasi ke backend

### Backend
- **FastAPI** (Python) -> REST API
- **Ultralytics YOLOv8** -> model deteksi & grading
- **SQLModel** + **Neon (Postgres)** -> database (opsional, untuk history hasil grading)
- **Uvicorn** -> ASGI server

### Deployment
- Frontend → Vercel / Netlify
- Backend → Railway / Render

> Tech stack di atas boleh disesuaikan/diganti **kalau ada alasan yang jelas** (misal ada yang lebih familiar dengan alternatif tertentu). Yang **tidak boleh**: mengganti bahasa backend jadi non-Python (karena model YOLO/ultralytics hanya jalan native di Python), atau mengganti pendekatan jadi native app (Flutter/Kotlin), sudah diputuskan pakai PWA karena harus cross-platform (Android + iOS) tanpa effort besar. Diskusikan dulu di grup sebelum mengubah apa pun di luar itu.

## Struktur Folder

```
pinangsort/
├── backend/          # FastAPI + model
│   ├── models/        # file model (.pt)
│   ├── main.py         # entry point API
│   └── requirements.txt
├── frontend/         # React PWA
│   ├── src/
│   └── package.json
└── README.md
```

## Cara Setup (Development)

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API akan jalan di `http://localhost:8000`. Dokumentasi otomatis ada di `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App akan jalan di `http://localhost:5173` (default Vite).

## Format API (kontrak antara backend & frontend)

### `POST /predict`
**Request:** `multipart/form-data` dengan field `file` (gambar)

**Response:**
```json
{
  "detections": [
    {"grade": "super", "confidence": 0.95, "bbox": [120, 80, 200, 160]},
    {"grade": "biasa", "confidence": 0.88, "bbox": [250, 90, 310, 150]}
  ],
  "summary": {"super": 1, "biasa": 1, "ampas": 0}
}
```
> Kalau format ini perlu berubah selama development, **update bagian ini di README dan kabari tim di grup** sebelum push, biar nggak ada yang kerja berdasarkan kontrak lama.

## Alur Kerja Tim (Branch-based)

Kita **tidak** pakai fork, semua kerja langsung di repo ini, pakai branch masing-masing. Ini repo kecil, tim cuma 3 orang, dan waktu terbatas.

### Aturan branch
- `main` -> branch stabil. **Jangan push langsung ke `main`.**
- Buat branch baru untuk tiap fitur/tugas, dengan format: `nama/deskripsi-singkat`
  - Contoh: `yoga/backend-predict-endpoint`, `melody/frontend-upload-page`

### Langkah kerja
```bash
git checkout main
git pull origin main
git checkout -b nama/fitur-yang-dikerjain

git add .
git commit -m "pesan commit yang jelas"
git push origin nama/fitur-yang-dikerjain
```
Lalu buka **Pull Request** ke `main` di GitHub, minta 1 anggota lain review sebelum merge (kalau waktu benar-benar mepet dan tidak sempat review, minimal kabari di grup sebelum merge sendiri).

### Aturan supaya nggak konflik
1. **Jangan edit file yang sedang dikerjakan orang lain** tanpa koordinasi dulu di grup.
2. **Pull `main` secara rutin** ke branch kamu (`git pull origin main`) supaya branch nggak terlalu jauh ketinggalan dan konflik saat merge nggak menumpuk.
3. **Commit kecil & sering**, jangan 1 commit raksasa di akhir, lebih gampang di-review dan di-debug kalau ada masalah.
4. **Jangan commit file besar/sensitive**: `.env`, `node_modules/`, `venv/`, dll, sudah diatur di `.gitignore`, jangan di-force-add.
5. Kalau nemu bug atau perlu ubah kontrak API (format request/response), **kabari di grup dulu** sebelum ubah, karena itu ngaruh ke kerjaan 2 orang lain.

## Pembagian Tugas

| Nama | Tugas |
|---|---|
| Yang Mulia Maha Kaisar | Backend (FastAPI), integrasi model YOLO, database |
| Nami | Frontend UI/UX (halaman upload, halaman hasil, styling, PWA setup) |
| zikruy | Frontend logic (integrasi ke API backend, state/error handling, fitur history) |

## Model

Model yang dipakai: **YOLOv8n-seg**, dilatih pada dataset [Sortir Pinang](https://universe.roboflow.com/nofbin-gofri/sortir-pinang-rhqly) (3 kelas: `ampas`, `biasa`, `super`), hasil test set mAP50 = 0.991.
