const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

// Define the ImageRecord schema
const imageRecordSchema = new Schema(
  {
    user_id: {
      type: Types.ObjectId,
      ref: 'users', // Reference to the User model
      required: true,
    },
    interview_id: {
      type: Types.ObjectId,
      ref: 'interview_templates', // Reference to the Interview model
      required: true,
    },
    question_id: {
      type: Types.ObjectId,
      ref: 'questions', // Reference to the Question model
      required: true,
    },
    filename: {
      type: String,
      required: true,
    },
    score: {
      type: Number,
      required: true,
    },
    emotions: {
      type: Map,
      of: String, // Assuming emotions is a map with string keys and string values (adjust as necessary)
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
);

// Create the Mongoose model
const ImageRecord = mongoose.model('image_records', imageRecordSchema);

module.exports = ImageRecord;
