const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the TranscriptionRecord schema
const transcriptionRecordSchema = new Schema(
  {
    user_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'users', // Reference to the User model
      required: true,
    },
    interview_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'interview_templates', // Reference to the Interview model
      required: true,
    },
    question_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'questions', // Reference to the Question model
      required: true,
    },
    filename: {
      type: String,
      required: true,
    },
    transcription: {
      type: String,
      required: true,
    },
    created_at: {
      type: Date,
      default: Date.now,
    },
    updated_at: {
      type: Date,
    },
  },
  { timestamps: true } // Automatically adds `created_at` and `updated_at` fields
);

// Create the Mongoose model
const TranscriptionRecord = mongoose.model('transcriptions', transcriptionRecordSchema);

module.exports = TranscriptionRecord;
