const mongoose = require('mongoose');

const dealershipSchema = new mongoose.Schema({
  id: Number,
  city: String,
  state: String,
  st: String,
  address: String,
  zip: String,
  lat: Number,
  long: Number,
  short_name: String,
  full_name: String
});

module.exports = mongoose.model('Dealership', dealershipSchema);
