require("dotenv").config(); // Load environment variables from .env file
const express = require("express");
const axios = require("axios"); // HTTP client for making requests
const FormData = require("form-data");
const router = express.Router();

const FACE_RECOGNITION_SERVICE_URL = process.env.FACE_RECOGNITION_SERVICE_URL; // Fetch from .env

if (!FACE_RECOGNITION_SERVICE_URL) {
    console.error("FACE_RECOGNITION_SERVICE_URL is not defined in the environment variables.");
    process.exit(1); // Exit if the variable is missing
}

router.get("/", async(req, res) => {
    const response = await axios.get(`${FACE_RECOGNITION_SERVICE_URL}/`);
    res.send(response.data);
});


// Route to handle the POST request
router.post("/analyse-image/", async (req, res) => {
    try {
      // Ensure the file is uploaded correctly
      if (!req.file) {
        return res.status(400).send({ error: "File is required" });
      }
  
      // Create FormData for forwarding to FastAPI
      const form = new FormData();
  
      // Append the audio file from multer's req.file (Buffer)
      form.append("file", req.file.buffer, { filename: req.file.originalname, contentType: req.file.mimetype });
  
      // Ensure we have the other form fields
      const { question_id, interview_id, user_id, company_id } = req.body;
  
      if (!question_id || !interview_id || !user_id || !company_id) {
        return res.status(400).send({
          error: "Missing required fields: question_id, interview_id, or user_id",
        });
      }
  
      // Append the other form fields
      form.append("question_id", question_id);
      form.append("interview_id", interview_id);
      form.append("user_id", user_id);
      form.append("company_id", company_id);
  
      // Forward the request to FastAPI
      const response = await axios.post(
        `${FACE_RECOGNITION_SERVICE_URL}/analyse-image/`,
        form,
        {
          headers: {
            ...form.getHeaders(),  // Include multipart/form-data headers
          },
        }
      );
  
      // Send the response from FastAPI back to the client
      res.status(response.status).send(response.data);
    } catch (error) {
      console.error("Error routing to Voice Analysis Service:", error.message);
  
      if (error.response) {
        res.status(error.response.status).send(error.response.data);
      } else {
        res.status(500).send({ error: "Failed to connect to Voice Analysis Service" });
      }
    }
});

module.exports = router;