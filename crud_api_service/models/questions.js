const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the Question schema
const questionSchema = new Schema(
  {
    question_text: {
      type: String,
      required: true,
    },
    category: {
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
);

// Create the Mongoose model
const Question = mongoose.model('questions', questionSchema);

module.exports = Question;
