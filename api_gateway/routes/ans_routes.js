require("dotenv").config(); // Load environment variables from .env file
const express = require("express");
const axios = require("axios"); // HTTP client for making requests
const router = express.Router();

const ANS_ANALYSIS_SERVICE_URL = process.env.ANS_ANALYSIS_SERVICE_URL; // Fetch from .env

if (!ANS_ANALYSIS_SERVICE_URL) {
    console.error("ANS_ANALYSIS_SERVICE_URL is not defined in the environment variables.");
    process.exit(1); // Exit if the variable is missing
}

router.post("/analyse-results/", async (req, res) => {
    try {
        // Forward the request to the face recognition service
        const response = await axios.post(`${FACE_RECOGNITION_SERVICE_URL}/analyse-results/`, req.body, {
            headers: req.headers, // Pass original headers if needed
        });

        // Return the response from the face recognition service to the client
        res.status(response.status).send(response.data);
    } catch (error) {
        console.error("Error routing to face recognition service:", error.message);

        // Handle errors gracefully
        if (error.response) {
            // If the error is from the face recognition service
            res.status(error.response.status).send(error.response.data);
        } else {
            // Other errors (network issues, etc.)
            res.status(500).send({ error: "Failed to connect to face recognition service" });
        }
    }
});

module.exports = router;
