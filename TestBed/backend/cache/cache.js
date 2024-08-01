const LOCAL_CACHE_URL = process.env["LOCAL_CACHE_URL"] || "redis://localhost:6379";
const REMOTE_CACHE_URL = process.env["REMOTE_CACHE_URL"] || "redis://localhost:6380";

const { createClient } = require("redis");
const logger = require("../logger/logger");

const CACHE_MODE = {
    LOCAL: "local",
    REMOTE: "remote"
}

const _create_redis_client = (url) => {
    let client = createClient({ url: url });
    client.on('error', err => logger.debug('Redis Client Error', err));
    return client;
}

const _cache_save_item = async (mode, item) => {
    try {
        let url = mode === CACHE_MODE.LOCAL ? LOCAL_CACHE_URL : REMOTE_CACHE_URL;
        let ttl = mode === CACHE_MODE.LOCAL ? 300 : 100;
        let key = item["index"];

        let client = _create_redis_client(url);
        await client.connect();
        if ((await client.exists(key)) == false)
        {
            await client.setEx(key, ttl, JSON.stringify(item));
        }
        await client.disconnect();
    } catch (err) {
        throw err;
    }
}

const remote_cache_save_item = async (item) => {
    try {
        await _cache_save_item(CACHE_MODE.REMOTE, item);
    } catch (err) {
        throw err;
    }
}

const local_cache_save_item = async (item) => {
    try {
        await _cache_save_item(CACHE_MODE.LOCAL, item);
    } catch (err) {
        throw err;
    }
}

const _cache_get_item = async (mode, index) => {
    try {
        let url = mode === CACHE_MODE.LOCAL ? LOCAL_CACHE_URL : REMOTE_CACHE_URL;

        let client = _create_redis_client(url);
        await client.connect();
        const jsonString = await client.get(index);
        await client.disconnect();
        if (jsonString)
        {
            const item = JSON.parse(jsonString);
            return item; 
        }
        return null;
    } catch (err) {
        throw err;
    }
}

const remote_cache_get_item = async (index) => {
    try {
        return await _cache_get_item(CACHE_MODE.REMOTE, index);
    } catch (err) {
        throw err;
    }
}

const local_cache_get_item = async (index) => {
    try {
        return await _cache_get_item(CACHE_MODE.LOCAL, index);
    } catch (err) {
        throw err;
    }
}

module.exports = {
    local_cache_get_item,
    local_cache_save_item,
    remote_cache_get_item,
    remote_cache_save_item
}