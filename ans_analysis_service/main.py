from sentence_transformers import SentenceTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from crud import create_score_record, create_audio_record, get_user_record, get_question_record, get_interview_template_record
from speech_to_text import convert_speech_to_text
from ans_analysis import evaluate_answer
from utils import generate_unique_filename, get_question_text, get_required_skills, get_culture_description
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

PORT = int(os.getenv("PORT", 5001))

app = FastAPI()

# Allow origins for CORS
origins = ["*"]  # Allow all origins for now

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load the sentiment analysis model
model = SentimentIntensityAnalyzer()

# Load the sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Emotion Recognition API!"}


@app.post("/analyse-results/")
async def transcribe_audio(file: UploadFile = File(...),  
    question_id: str = Form(...),
    interview_id: str = Form(...),
    company_id: str = Form(...),
    user_id: str = Form(...)):
    # Check if file is received

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check if the uploaded file is an audio file
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an audio file")

    # Generate unique filename and save the file to disk
    unique_filename = generate_unique_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    print('Content-Type:', file.content_type)

    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"File saved to {file_path}")

        
        # Analyze emotions
        text = convert_speech_to_text(file_path)
        print("Text detected:", text)

        if not isinstance(text, str):
            raise ValueError("Transcription did not return a string.")
        
        timestamp = datetime.now().isoformat()
        record = {
            "filename": file.filename,
            "transcription": text,
            "created_at": timestamp,
            "question_id": ObjectId(question_id),
            "interview_id": ObjectId(interview_id),
            "user_id": ObjectId(user_id),
        }

        record_id = await create_audio_record(record)
        print(f"Record saved with ID: {record_id}")  # Log the record ID returned

        if not isinstance(record_id, (str, int)):
            raise ValueError("Invalid record ID returned from database.")

        question_text = await get_question_text(question_id)
        culture_reference_texts = await get_culture_description(company_id)
        required_skills = await get_required_skills(interview_id)

        if(question_text is None or culture_reference_texts is None or required_skills is None):
            raise ValueError("Question, culture reference texts, or required skills not found in database.")

        results = evaluate_answer(question_text, text, model, sentence_model, culture_reference_texts, required_skills)
        # Add additional data to the dictionary
        results["created_at"] = timestamp
        results["filename"] = file.filename
        results["question_id"] = ObjectId(question_id),
        results["interview_id"] = ObjectId(interview_id),
        results["user_id"] = ObjectId(user_id),

        print("Evaluation Results:", results)

        # Save the transcription to the database
        record_id = await create_score_record(results)
        print(f"Record saved with ID: {record_id}")  # Log the record ID returned

        if not isinstance(record_id, (str, int)):
            raise ValueError("Invalid record ID returned from database.")
        
    
    except Exception as e:
        print(f"Error processing audio file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

    finally:
        # Clean up temporary file after sending the request or on error
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Temporary file {file_path} removed successfully.")
        except Exception as e:
            print(f"Error removing temporary file: {e}")

    return {"id": record_id, "transcription": text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False)