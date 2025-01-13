const express= require("express");
const cors= require("cors");
const bodyParser= require("body-parser");
const face= require("./routes/face_routes");
const ans= require("./routes/ans_routes");
const crud= require("./routes/crud_routes");
const voice= require("./routes/voice_routes");
const multer= require("multer");
require("dotenv").config();

const PORT = process.env.PORT || 8000;

const app= express();
const upload = multer(); 

app.set('env', 'production');
app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));
app.use(upload.single("file"))

app.use(cors({
  origin: "*",
  credentials: true
}));


app.use("/face", face);
app.use("/audio", voice);
app.use("/ans", ans);
app.use("/crud", crud);


app.listen(PORT, () => {
    console.log(`server listening on port: ${PORT}`);
})