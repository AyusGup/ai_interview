const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

// Define the InterviewTemplate schema
const interviewTemplateSchema = new Schema(
  {
    questions: [
      {
        type: Types.ObjectId,
        ref: 'questions', // Reference to the Question model
        required: true,
      },
    ],
    experience_keywords: [
      {
        type: String,
        required: true,
      },
    ],
    created_at: {
      type: Date,
      default: Date.now,
    },
    updated_at: {
      type: Date,
    },
  },
);

// Create the Mongoose model
const InterviewTemplate = mongoose.model('interview_templates', interviewTemplateSchema);

module.exports = InterviewTemplate;
