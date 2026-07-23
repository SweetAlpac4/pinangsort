import io

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from ultralytics import YOLO

app = FastAPI(title="PinangSort API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: persempit ke domain frontend pas udah deploy
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model sekali aja saat startup, bukan tiap request (biar cepat)
model = YOLO("models/pinang_model.pt")


@app.get("/")
def root():
    return {"status": "PinangSort API is running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # baca file upload jadi gambar PIL
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # jalanin inference
    results = model(image)
    result = results[0]

    detections = []
    summary = {"super": 0, "biasa": 0, "ampas": 0}

    for box in result.boxes:
        class_id = int(box.cls[0])
        grade = model.names[class_id]  # "ampas" / "biasa" / "super"
        confidence = float(box.conf[0])
        bbox = [round(x, 1) for x in box.xyxy[0].tolist()]  # [x1, y1, x2, y2]

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
