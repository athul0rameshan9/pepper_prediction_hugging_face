# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import tempfile
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

@app.post("/api/predict")
async def predict(imgFile: UploadFile = File(...), hdrFile: UploadFile = File(...)):
    try:
        # Check file types
        if not imgFile.filename.endswith('.img') or not hdrFile.filename.endswith('.hdr'):
            raise HTTPException(status_code=400, detail="Invalid file types. Upload .img and .hdr files.")

        # Create temporary files for img and hdr
        with tempfile.NamedTemporaryFile(delete=False) as img_temp, tempfile.NamedTemporaryFile(delete=False) as hdr_temp:
            img_path = img_temp.name
            hdr_path = hdr_temp.name

            # Save img and hdr to temporary files
            with open(img_path, "wb") as f:
                shutil.copyfileobj(imgFile.file, f)

            with open(hdr_path, "wb") as f:
                shutil.copyfileobj(hdrFile.file, f)

            # Call your prediction function
            result = predict_moisture(img_path, hdr_path)

            # Clean up the temporary files
            os.remove(img_path)
            os.remove(hdr_path)

            # Check prediction result
            if "error" in result:
                return JSONResponse(status_code=500, content={"error": result["error"]})

            # Return prediction results
            return {
                "moisture": result.get("moisture_prediction"),
                "piperine": result.get("piperine_prediction")
            }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during prediction: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

