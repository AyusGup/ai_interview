const transcriptions = require('./models/transcriptions');
const images = require('./models/images');
const scores = require('./models/scores');
const questions = require('./models/questions');
const interviews = require('./models/interviews');
const users = require('./models/users');
const interview_templates = require('./models/interview_template');


// Get an image record by ID
async function getImageRecord(id) {
    const record = await images.findOne({ _id: id });
    return record;
}

// Get all image records
async function getAllImageRecords() {
    const records = await images.find();
    return records;
}

// Create question record
async function createQuestionRecord(questionData) {
    const question = new questions(questionData);
    const result = await question.save();
    return result._id.toString();
}

// Get question record by ID
async function getQuestionRecord(questionId) {
    const question = await questions.findOne({ _id: questionId });
    return question;
}

// Get all questions
async function getAllQuestions() {
    const questions = await questions.find();
    return questions;
}

// Create interview template record
async function createInterviewDB(interviewData) {
    const interview = new interview_template(interviewData);
    const result = await interview.save();
    return result._id.toString();
}

// Get interview template record by ID
async function getInterviewTemplateRecord(interviewTemplateId) {
    const interviewTemplate = await interview_templates.findOne({ _id: interviewTemplateId });
    return interviewTemplate;
}

// Get all interview templates
async function getAllInterviews() {
    const interviews = await interview_templates.find();
    return interviews;
}

// Get user record by ID
async function getUserRecord(userId) {
    const user = await users.findOne({ _id: userId });
    return user;
}

// Get all scores
async function getScores() {
    try {
        const response = await images.find().populate('question_id').populate('interview_id').populate('user_id');
        return response;
    } catch (error) {
        console.error('Error fetching scores:', error);
    }
}

module.exports = {
    getImageRecord,
    getAllImageRecords,
    createQuestionRecord,
    getQuestionRecord,
    getAllQuestions,
    createInterviewDB,
    getInterviewTemplateRecord,
    getAllInterviews,
    getUserRecord,
    getScores
};
