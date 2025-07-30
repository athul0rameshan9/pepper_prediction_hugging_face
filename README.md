# 🌶️ Pepper Quality Prediction

This project predicts **piperine** and **moisture content** in pepper samples using **hyperspectral images**.

It has two parts:
- 🧠 A **FastAPI backend** hosted on **Hugging Face Spaces**
- 🌐 A **simple HTML + JavaScript frontend** hosted on **Vercel**

---

## 🔗 Live Links

- 🚀 **Frontend (Vercel)**: [https://pepper-predictor.vercel.app](https://pepper-predictor.vercel.app)
- 🧠 **Backend API (Hugging Face)**: [https://huggingface.co/spaces/athul0rameshan9/pepper_predictor](https://huggingface.co/spaces/athul0rameshan9/pepper_predictor)

---

## 🧠 What It Does

- Accepts a **hyperspectral image** of a pepper sample
- Sends it to the backend using a `POST` request
- Returns:
  - **Piperine content (%)**
  - **Moisture content (%)**

---

## ⚙️ Tech Stack

| Component    | Technology              |
|--------------|--------------------------|
| Backend      | FastAPI, scikit-learn    |
| Frontend     | HTML, JavaScript         |
| Image Utils  | OpenCV, NumPy            |
| Backend Host | Hugging Face Spaces      |
| Frontend Host| Vercel                   |

---

## 🚀 Usage

### 🔸 Web Interface

1. Visit the **Frontend**: [https://pepper-predictor.vercel.app](https://pepper-predictor.vercel.app)
2. Upload a hyperspectral image (JPG/PNG)
3. Get instant prediction of **piperine** and **moisture** content

### 🔸 API Usage

You can also use the backend directly via `POST` request.

#### Example in Python

```python
import requests

url = "https://athul0rameshan9-pepper_predictor.hf.space/predict"
files = {'file': open('sample_image.png', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```
Expected Response
json
Copy
Edit
{
  "piperine_content": 4.21,
  "moisture_content": 13.35
}
📁 Project Structure
bash
Copy
Edit
pepper_prediction_hugging_face/
├── main.py              # FastAPI backend
├── model.joblib         # Trained model
├── utils.py             # Image processing functions
├── requirements.txt     # Python dependencies
└── frontend/            # (Deployed separately on Vercel)
    ├── index.html       # HTML page
    ├── script.js        # JS to send image to API
    └── style.css        # Optional styling
🧪 Deployment
Frontend is deployed on Vercel

Backend is deployed on Hugging Face Spaces

The frontend sends a POST request to the Hugging Face backend using the /predict endpoint.



