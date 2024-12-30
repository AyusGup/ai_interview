from uuid import uuid4
import time
from crud import get_user_record, get_question_record, get_interview_template_record

# Generate a unique filename for uploaded files
def generate_unique_filename(original_filename):
    timestamp = str(int(time.time() * 1000))  # Millisecond precision
    random_uuid = str(uuid4())  # Generate a unique UUID
    unique_filename = f"{timestamp}_{random_uuid}_{original_filename}"
    return unique_filename

# Get culture description by user id
async def get_culture_description(user_id: str):
    user = await get_user_record(user_id)
    return user["culture_description"]

# Get question by id
async def get_question_text(question_id: str):
    question = await get_question_record(question_id)
    return question['question_text']

# Get required skills by interview id
async def get_required_skills(interview_id: str):
    interview = await get_interview_template_record(interview_id)
    return interview['experience_keywords']
