const express= require("express");
const cors= require("cors");
const bodyParser= require("body-parser");
const fileupload = require("express-fileupload");
const mongoose = require("./config/db");
require("dotenv").config();
const { createInterviewDB, createQuestionRecord, getScores } = require("./crud");
const PORT = process.env.PORT || 5003;

const app= express();

app.set('env', 'production');
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb',extended:true}));
app.use(fileupload({
  useTempFiles: true,
}))

app.use(cors({
  origin: "*",
  credentials: true
}));

app.post("/create-interview", async (req, res) => {
  const interviewData = req.body;
  const result = await createInterviewDB(interviewData);
  return res.send(result);
});

app.post("/create-question", async (req, res) => {
  const questionData = req.body;
  const result = await createQuestionRecord(questionData);
  return res.send(result);
});

app.get("/test", async (req, res) => {
  const scores = await getScores();
  return res.send(scores);
});

app.get("/", async (req, res) => {
  return res.send("Hello World");
});

app.listen(PORT, () => {
    console.log(`server listening on port: ${PORT}`);
})