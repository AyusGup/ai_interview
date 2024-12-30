from mongoengine import (
    Document, StringField, ReferenceField, DateTimeField, 
    ListField, DictField
)
from datetime import datetime
from bson import ObjectId


# User Model
class User(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    culture_description = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()


# Question Model
class Question(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    question_text = StringField(required=True)
    category = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()


# InterviewTemplate Model
class InterviewTemplate(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    questions = ListField(ReferenceField(Question))  # Reference to Question documents
    culture_description = StringField(required=True)
    experience_keywords = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()


# Interview Model
class Interview(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    company_id = ReferenceField(User)  # Reference to the User document (company)
    user_id = ReferenceField(User)  # Reference to the User document (candidate)
    interview_template_id = ReferenceField(InterviewTemplate)  # Reference to InterviewTemplate
    status = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()


# ImageRecord Model
class ImageRecord(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    user_id = ReferenceField(User)  # Reference to the User document
    interview_id = ReferenceField(InterviewTemplate)  # Reference to the Interview document
    question_id = ReferenceField(Question)  # Reference to the Question document
    filename = StringField(required=True)
    score = StringField(required=True)
    emotions = DictField()  # Store emotions as a dictionary
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()


# TranscriptionRecord Model
class TranscriptionRecord(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    user_id = ReferenceField(User)  # Reference to the User document
    interview_id = ReferenceField(Interview)  # Reference to the Interview document
    question_id = ReferenceField(Question)  # Reference to the Question document
    filename = StringField(required=True)
    transcription = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()


# ScoreRecord Model
class ScoreRecord(Document):
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))
    user_id = ReferenceField(User)  # Reference to the User document
    interview_id = ReferenceField(Interview)  # Reference to the Interview document
    question_id = ReferenceField(Question)  # Reference to the Question document
    filename = StringField(required=True)
    positivity = StringField(required=True)
    culture_fit = StringField(required=True)
    relevance = StringField(required=True)
    experience = StringField(required=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()
