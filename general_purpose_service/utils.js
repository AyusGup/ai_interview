const { v4: uuidv4 } = require('uuid');


function generateUniqueFilename(originalFilename) {
    const timestamp = Date.now();  // Millisecond precision
    const randomUuid = uuidv4();  // Generate a unique UUID
    const uniqueFilename = `${timestamp}_${randomUuid}_${originalFilename}`;
    return uniqueFilename;
}

async function getCultureDescription(userId) {
    try {
        const response = await axios.get(`your_database_endpoint/users/${userId}`);
        return response.data.culture_description;
    } catch (error) {
        console.error('Error fetching culture description:', error);
    }
}

async function getQuestionText(questionId) {
    try {
        const response = await axios.get(`your_database_endpoint/questions/${questionId}`);
        return response.data.question_text;
    } catch (error) {
        console.error('Error fetching question text:', error);
    }
}

async function getRequiredSkills(interviewId) {
    try {
        const response = await axios.get(`your_database_endpoint/interviews/${interviewId}`);
        return response.data.experience_keywords;
    } catch (error) {
        console.error('Error fetching required skills:', error);
    }
}

module.exports = {
    generateUniqueFilename,
    getCultureDescription,
    getQuestionText,
    getRequiredSkills,
};
