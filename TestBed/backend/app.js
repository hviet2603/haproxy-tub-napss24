const express = require("express");
const mongoose = require("mongoose");
const item_router = require("./routes/item_router");

const { MONGO_CONNECT_URL, BACKEND_NAME } = require("./config/config");

let app = express();

app.get("/", (req, res) => {
    res.send(`<h1>${BACKEND_NAME} says hello!<h1>`)
})

app.use("/items", item_router);

mongoose.connect(MONGO_CONNECT_URL).then(() => {
    app.listen(3000);
})