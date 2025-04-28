# main.py
import tempfile
import shutil
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model import predict_moisture  # Import your model function here

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

# Path to save the uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if not os.access(UPLOAD_DIR, os.W_OK):
    print(f"Error: Cannot write to {UPLOAD_DIR}. Check permissions.")
else:
    print(f"{UPLOAD_DIR} is writable.")


@app.post("/api/predict")
async def predict(imgFile: UploadFile = File(...), hdrFile: UploadFile = File(...)):
    try:
        # Print received files info
        print(f"Received files: {imgFile.filename}, {hdrFile.filename}")

        # Check file types
        if not imgFile.filename.endswith('.img') or not hdrFile.filename.endswith('.hdr'):
            raise HTTPException(status_code=400, detail="Invalid file types. Upload .img and .hdr files.")

        # Save the uploaded files to the server
        img_path = os.path.join(UPLOAD_DIR, imgFile.filename)
        hdr_path = os.path.join(UPLOAD_DIR, hdrFile.filename)

        print(f"Saving files to: {img_path}, {hdr_path}")

        with open(img_path, "wb") as f:
            shutil.copyfileobj(imgFile.file, f)
        with open(hdr_path, "wb") as f:
            shutil.copyfileobj(hdrFile.file, f)

        print(f"Files saved: {img_path}, {hdr_path}")

        # Call your prediction function and pass the file paths
        result = predict_moisture(img_path, hdr_path)
        print(f"Prediction result: {result}")

        # Clean up the uploaded files after prediction
        os.remove(img_path)
        os.remove(hdr_path)

        # Check prediction result
        if "error" in result:
            print(f"Prediction error: {result['error']}")
            return JSONResponse(status_code=500, content={"error": result["error"]})

        # Return prediction results
        return {
            "moisture": result.get("moisture_prediction"),
            "piperine": result.get("piperine_prediction")
        }

    except Exception as e:
        print(f"An error occurred during prediction: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during prediction: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
