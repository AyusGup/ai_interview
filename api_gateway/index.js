const express= require("express");
const cors= require("cors");
const bodyParser= require("body-parser");
const face= require("./routes/face_routes");
const ans= require("./routes/ans_routes");
const general= require("./routes/general_routes");
const fileupload= require("express-fileupload");
require("dotenv").config();

const PORT = process.env.PORT || 8000;

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


app.use("/face",face);
app.use("/ans",ans);
app.use("/general", general);


app.listen(PORT, () => {
    console.log(`server listening on port: ${PORT}`);
})