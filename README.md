# Accident-Report-AI 🚗🤖  

AI-powered tool for insurance accident reports that:  
- Extracts text from PDFs.  
- Detects vehicle damages in uploaded images (scratches, dents, broken lamps, etc.).  
- Compares results and generates a final matching score with comments.  
- Supports **multiple languages** (English, French, Arabic, …).  

---

## 📸 Demo Screenshot  

![Accident Report Demo](./image_2025-09-22_15-06-50.png)  

---

## ⚙️ Features  

- **PDF Text Extraction** → Extract structured accident report data.  
- **Damage Detection** → YOLO-based AI model for detecting car damages.  
- **Comparison Engine** → Matches detected damages with PDF declarations.  
- **Multi-Language Support** → Expands usage to global insurance markets.  

---

## 🚀 Tech Stack  

- **Python**  
- **YOLO (Ultralytics)** for object detection  
- **OpenCV** & **Pillow** for image processing  
- **pdfplumber** for PDF parsing  
- **Deep-Translator** for multi-language support  
---

## 🛠️ Installation  

```bash
# Clone the repository
git clone https://github.com/YourUsername/Accident-Report-AI.git

# Navigate to project folder
cd Accident-Report-AI

# Install dependencies
pip install -r requirements.txt

```
---

## ⚙️ How to Use
1. Upload the accident PDF report.  
2. Upload vehicle images.  
3. The system detects damages and compares with PDF descriptions.  
4. Get a **final percentage match** + comment about the consistency.  

---

## 📌 Future Work
- Web interface for uploading PDFs & images  
- API integration with insurance platforms  
- More damage categories for detection  

---

## 📄 License
This project is released under the **MIT License**.  


