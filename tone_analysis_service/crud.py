from database import database
from bson import ObjectId

question_collection = database["questions"]
interview_template_collection = database["interview_templates"]
user_collection = database["users"]
transcription_collection = database['transcriptions']
score_collection = database['scores']
audio_collection = database['audio_records']

# Function to create a transcription record
async def create_audio_record(record: dict):
    result = await transcription_collection.insert_one(record)
    return str(result.inserted_id)

# Create a new score record
async def create_score_record(record: dict):
    result = await score_collection.insert_one(record)
    return str(result.inserted_id)

# Get question record by id
async def get_question_record(question_id: str):
    result = await question_collection.find_one({"_id": ObjectId(question_id)})
    return result

# get interview template record by id
async def get_interview_template_record(interview_template_id: str):
    result = await interview_template_collection.find_one({"_id": ObjectId(interview_template_id)})
    return result

# Get user by id
async def get_user_record(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return user

async def create_tone_record(record: dict) -> str:
    result = await audio_collection.insert_one(record)
    return str(result.inserted_id)