const mongoose = require('mongoose');
const { Schema } = mongoose;

const ItemSchema = new Schema({ 
    index: {
        type: String,
        required: true
    },
    value: {
        type: String,
        required: true
    },
    _backend: {
        type: String,
        required: true
    } 
});

const Item = mongoose.model('Item', ItemSchema);

module.exports = Item;