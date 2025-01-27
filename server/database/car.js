const mongoose = require('mongoose');

const carSchema = new mongoose.Schema({
  id: Number,
  dealer_id: Number,
  year: Number,
  make: String,
  model: String,
  type: String,
  mileage: Number,
  fuel: String,
  transmission: String,
  engine: String,
  price: Number
});

module.exports = mongoose.model('Car', carSchema);