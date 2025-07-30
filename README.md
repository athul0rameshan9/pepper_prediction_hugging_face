# 🌶️ Pepper Quality Prediction API

This project predicts **piperine** and **moisture content** in pepper samples using **hyperspectral images**.

It uses a **FastAPI** backend and a lightweight **HTML + JavaScript frontend**, and is deployed on **Hugging Face Spaces**.

🔗 **Live Demo**: [https://huggingface.co/spaces/athul0rameshan9/pepper_predictor](https://huggingface.co/spaces/athul0rameshan9/pepper_predictor)

---

## 🧠 What It Does

- Accepts a **hyperspectral image** of pepper (as a `.png` or `.jpg`)
- Processes the image on the backend
- Returns predicted:
  - **Piperine content (%)**
  - **Moisture content (%)**

---

## ⚙️ Tech Stack

| Component  | Tech Used           |
|------------|---------------------|
| Backend    | FastAPI             |
| Frontend   | HTML, CSS, JavaScript |
| Deployment| Hugging Face Spaces |
| ML Model   | scikit-learn        |
| Image Processing | OpenCV, NumPy |

---

## 🚀 Usage

### 🔸 Web UI

You can upload an image via the browser at the [Live Demo](https://huggingface.co/spaces/athul0rameshan9/pepper_predictor).

### 🔸 API (Programmatic Access)

Send a POST request with the image file.

#### Example (Python)

```python
import requests

url = "https://athul0rameshan9-pepper_predictor.hf.space/predict"
files = {'file': open('sample.png', 'rb')}

res = requests.post(url, files=files)
print(res.json())
'''
