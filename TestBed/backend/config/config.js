const MONGO_CONNECT_URL = process.env["MONGO_CONNECT_URL"] || "mongodb://admin:admin@localhost:27017/";
const BACKEND_NAME = process.env["BACKEND_NAME"] || "Backend";

module.exports = {
    MONGO_CONNECT_URL,
    BACKEND_NAME
}