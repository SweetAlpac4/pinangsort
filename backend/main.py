import io
import logging
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pinangsort")

app = FastAPI(title="PinangSort API")

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = (
    ["*"] if allowed_origins_env == "*" else allowed_origins_env.split(",")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = YOLO("models/pinang_model.pt")
    logger.info("Model berhasil dimuat.")
except Exception:
    logger.exception("Gagal memuat model.")
    raise


@app.get("/")
def root():
    return {
        "status": "PinangSort API is running",
        "model_loaded": model is not None,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File yang diupload harus berupa gambar (jpg/png/dll).",
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        logger.exception("Gagal membaca file sebagai gambar.")
        raise HTTPException(
            status_code=400,
            detail="File tidak dapat dibaca sebagai gambar. Pastikan file tidak rusak.",
        )

    try:
        results = model(image)
        result = results[0]
    except Exception:
        logger.exception("Inference model gagal.")
        raise HTTPException(
            status_code=500,
            detail="Terjadi kesalahan saat memproses gambar. Coba lagi.",
        )

    detections = []
    summary = {"super": 0, "biasa": 0, "ampas": 0}

    for box in result.boxes:
        class_id = int(box.cls[0])
        grade = model.names[class_id]  
        confidence = float(box.conf[0])
        bbox = [round(x, 1) for x in box.xyxy[0].tolist()]  

        detections.append({
            "grade": grade,
            "confidence": round(confidence, 4),
            "bbox": bbox,
        })
        summary[grade] += 1

    return {
        "detections": detections,
        "summary": summary,
    }
