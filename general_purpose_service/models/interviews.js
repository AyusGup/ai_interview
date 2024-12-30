const mongoose = require('mongoose');
const { Schema, Types } = mongoose;

// Define the Interview schema
const interviewSchema = new Schema(
  {
    company_id: {
      type: Types.ObjectId,
      ref: 'users', // Reference to the User model for the company
      required: true,
    },
    user_id: {
      type: Types.ObjectId,
      ref: 'users', // Reference to the User model for the interviewee
      required: true,
    },
    interview_template_id: {
      type: Types.ObjectId,
      ref: 'interview_templates', // Reference to the InterviewTemplate model
      required: true,
    },
    status: {
      type: String,
      required: true,
      enum: ['pending', 'completed', 'in-progress'], // Example statuses, adjust as needed
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
const Interview = mongoose.model('interviews', interviewSchema);

module.exports = Interview;
