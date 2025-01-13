const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the ScoreRecord schema
const scoreRecordSchema = new Schema(
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
    positivity: {
      type: Number,
      required: true,
    },
    culture_fit: {
      type: Number,
      required: true,
    },
    relevance: {
      type: Number,
      required: true,
    },
    experience: {
      type: Number,
      required: true,
    },
    created_at: {
      type: Date,
      default: Date.now,
    },
    updated_at: {
      type: Date,
    },
  }
);

// Create the Mongoose model
const ScoreRecord = mongoose.model('scores', scoreRecordSchema);

module.exports = ScoreRecord;
