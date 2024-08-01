const logger = require("../logger/logger");
const Item = require("../models/item");

const { BACKEND_NAME } = require("../config/config");
const { local_cache_get_item, local_cache_save_item } = require("../cache/cache");

const _get_item = async (index) =>  {
    try {
        let item = await local_cache_get_item(index);
        
        if (item) 
        {
            logger.info(`${BACKEND_NAME}: Local cache hit for index ${index}`);
            return item;
        } else {
            logger.info(`${BACKEND_NAME}: Local cache missed for index ${index}`);
            item = await Item.findOne({"index": index}, { _id: 0, __v: 0 }).exec();
        }

        if (item)
        {
            if (item["_backend"] === BACKEND_NAME)
            {
                await local_cache_save_item(item);
            }
        }

        return item;
    } catch (err) {
        throw err;
    }
}

const _post_item = async (item) => {
    try {
        let itemDAO = new Item({ ...item });
        let id = (await itemDAO.save())._id.toString();
        await local_cache_save_item(item);
        return id;
    } catch (err) {
        throw err;
    }
}

const get_item = async (req, res) => {
    try {
        if (req.query["id"] == null)
        {
            return res.status(400).end("Query param id required."); 
        }
        else
        {
            let index = req.query["id"];
            logger.info(`GET Item with the index ${index}.`);
            let item = await _get_item(index);
            if (item == null)
            {
                return res.status(404).json("Not found!");    
            }
            return res.json(item); 
        }
    }
    catch (err)
    {
        res.status(500).end(err.message);
    }
}

const post_item = async (req, res) => {
    try {
        if (req.body["index"] == null || req.body["index"] == undefined  
            || req.body["value"] == null || req.body["value"] == undefined)
        {
            return res.status(400).end("Request body invalid!");
        }
        if (await Item.exists({"index": req.body["index"]}))
        {
            return res.status(400).end("Item existed!");
        }
        let item = {
            ...req.body,
            _backend: BACKEND_NAME
        }
        logger.info(`POST Item ${JSON.stringify(item)}.`);
        let id = await _post_item(item);

        res.status(201).end(BACKEND_NAME);
    }
    catch (err)
    {
        res.status(500).end(err.message);
    }
}

module.exports = {
    get_item,
    post_item
}