# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from model import predict_moisture  # <--- Import your model function here

import uvicorn

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/predict")
async def predict(imgFile: UploadFile = File(...), hdrFile: UploadFile = File(...)):
    try:
        # Check file types
        if not imgFile.filename.endswith('.img') or not hdrFile.filename.endswith('.hdr'):
            raise HTTPException(status_code=400, detail="Invalid file types. Upload .img and .hdr files.")

        # Save uploaded files temporarily
        img_path = os.path.join(UPLOAD_DIR, imgFile.filename)
        hdr_path = os.path.join(UPLOAD_DIR, hdrFile.filename)

        print(img_path,hdr_path)

        with open(img_path, "wb") as f:
            shutil.copyfileobj(imgFile.file, f)

        with open(hdr_path, "wb") as f:
            shutil.copyfileobj(hdrFile.file, f)

        # Call prediction
        result = predict_moisture(img_path, hdr_path)

        # Clean up uploaded files
        os.remove(img_path)
        os.remove(hdr_path)

        # Check prediction result
        if "error" in result:
            return JSONResponse(status_code=500, content={"error": result["error"]})

        return {
            "moisture": result["moisture_prediction"],
            "piperine": result["piperine_prediction"]
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during prediction: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
