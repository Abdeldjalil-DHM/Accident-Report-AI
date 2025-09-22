# ==========================
# Accident Report Checker
# ==========================

# 1) Imports
import os
import pdfplumber
from deep_translator import GoogleTranslator
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
from google.colab import files

# ==========================
# 2) Load YOLO model
# ==========================
MODEL_PATH = "trained.pt" 
if not os.path.exists(MODEL_PATH):
    raise SystemExit("❌ Model not found. Upload trained.pt to the project folder.")

model = YOLO(MODEL_PATH)
print("✅ Model loaded. Classes:", model.names)

# ==========================
# 3) Synonyms + Normalize
# ==========================
synonyms = {
    "vitre cassée": "shattered glass",
    "pare-brise cassé": "shattered glass",
    "pneu crevé": "flat tire",
    "roue plate": "flat tire",
    "lumière cassée": "broken lamp",
    "feu cassé": "broken lamp",
    "ضوء مكسور": "broken lamp",
    "خدش": "scratch",
    "خوشة": "scratch",
    "طعجة": "dent",
    "凹み": "dent",
    "شق": "crack",
    "كسر": "crack"
}

def normalize_text(text: str) -> str:
    text = text.lower()
    for k, v in synonyms.items():
        if k in text:
            text = text.replace(k, v)
    try:
        text = GoogleTranslator(source='auto', target='en').translate(text)
    except:
        pass
    return text.lower()

# ==========================
# 4) PDF parsing
# ==========================
def parse_pdf(pdf_path):
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                texts.append(txt)
    return texts

# ==========================
# 5) YOLO Detection
# ==========================
def detect_images(img_paths, conf=0.25):
    detected = []
    for p in img_paths:
        results = model(p, conf=conf)
        r = results[0]

        annotated = r.plot()
        plt.figure(figsize=(7, 5))
        plt.imshow(annotated[:, :, ::-1])
        plt.axis("off")
        plt.show()

        if r.boxes is not None:
            for cid in r.boxes.cls.cpu().numpy().astype(int):
                detected.append(model.names[cid])
    return detected

# ==========================
# 6) Compare text vs detection
# ==========================
def compare_text_vs_detected(texts, detected_labels, MIN_MATCH=50):
    key_damages = ["shattered_glass", "flat_tire", "broken_lamp", "dent", "scratch", "crack"]

    joined_text = " ".join(texts)
    translated = normalize_text(joined_text)

    matches = {k: {"text": False, "image": False} for k in key_damages}

    for dmg in key_damages:
        if dmg.replace("_", " ") in translated or dmg in translated:
            matches[dmg]["text"] = True
        if any(dmg == det for det in detected_labels):
            matches[dmg]["image"] = True

    total = len(key_damages)
    identical = sum(1 for _, v in matches.items() if v["text"] and v["image"])
    percent = (identical / total) * 100

    print("\n=== COMPARISON REPORT ===")
    for dmg, status in matches.items():
        print(f"{dmg}: text={status['text']}, image={status['image']}")
    print(f"\nIDENTICAL = {identical}/{total} ({percent:.1f}%)")

    if percent >= MIN_MATCH:
        print(f"✅ Match is acceptable (≥{MIN_MATCH}%)")
    else:
        print(f"⚠️ Match is weak (<{MIN_MATCH}%)")

    return percent, matches

# ==========================
# 7) Run Example
# ==========================
if __name__ == "__main__":
    print("📄 Upload accident PDF")
    pdf_uploaded = files.upload()
    PDF_PATH = list(pdf_uploaded.keys())[0]

    texts = parse_pdf(PDF_PATH)

    print("🖼️ Upload accident photo(s)")
    img_uploaded = files.upload()
    IMG_PATHS = list(img_uploaded.keys())

    detected = detect_images(IMG_PATHS)
    compare_text_vs_detected(texts, detected, MIN_MATCH=50)
