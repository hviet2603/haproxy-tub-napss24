const express = require("express");
const { Router } = express;
const { get_item , post_item } = require("../controllers/item_controller");

let item_router = Router();

item_router.get("/", get_item);
item_router.post("/", express.json(), post_item);

module.exports = item_router;