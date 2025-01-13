import os
import shutil
import torch
import uvicorn
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import Wav2Vec2Model
from ml_model import FineTunedWav2Vec2Model
from get_score import get_score
from utils import generate_unique_filename
from dotenv import load_dotenv
from crud import create_tone_record
from bson import ObjectId

load_dotenv()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

PORT = int(os.getenv("PORT", 5002))

app = FastAPI()

# Allow all origins for CORS
origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Wav2Vec2 Emotion Recognition API!"}

@app.post("/analyse-audio/")
async def analyze_emotion(file: UploadFile = File(...),
    question_id: str = Form(...),
    interview_id: str = Form(...),
    user_id: str = Form(...)):

    # Check if file is received
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Ensure uploaded file is an audio file
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an audio file")

    # Generate a unique filename and save the file
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    print(file.file)
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"File saved to {file_path}")

        # Process the audio file to get the emotion score
        score = get_score(file_path, model, device)
        print(f"Emotion score: {score}")

        # Log the result with a timestamp
        timestamp = datetime.now().isoformat()
        result = {
            "filename": file.filename,
            "user_id": ObjectId(user_id),
            "interview_id": ObjectId(interview_id),
            "question_id": ObjectId(question_id),
            "score": (score[0]),
            "emotions": score[1],
            "created_at": timestamp,
        }
        print("Result:", result)

        # Save the result to the database
        record_id = await create_tone_record(result)
        print(f"Record saved with ID: {record_id}")  # Log the record ID returned

        if not isinstance(record_id, (str, int)):
            print(f"Invalid record ID type. Value: {record_id}, Type: {type(record_id)}")
            raise ValueError(f"Invalid record ID type: {type(record_id)}")


    except Exception as e:
        print(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

    finally:
        # Remove the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Temporary file {file_path} removed successfully.")

    return {"id": record_id, "emotions": score[1], "score": score[0]}


if __name__ == "__main__":
    # Load pre-trained Wav2Vec2 base model
    print("Loading Wav2Vec2 model...")  # Add here
    wav2vec2_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base", output_hidden_states=True).to(device)

    # Load fine-tuned model
    model = FineTunedWav2Vec2Model(wav2vec2_model, output_size=8).to(device)
    model.load_state_dict(torch.load("emotion_model.pth", map_location=device))
    model.eval()
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
