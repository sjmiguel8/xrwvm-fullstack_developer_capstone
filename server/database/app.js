const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())

const dealershipData = require('./data/dealerships.json');
const reviewData = require('./data/reviews.json');
const carData = require('./data/car_records.json');
const bodyParser = require('body-parser');
app.use(bodyParser.json());



const mongoURI = process.env.MONGODB_URI || "mongodb://localhost:27019/dealershipsDB";
mongoose.connect(mongoURI, {
  serverSelectionTimeoutMS: 5000,
  retryWrites: true
}).then(() => {
  console.log('Connected to MongoDB');
}).catch(err => {
  console.error('MongoDB connection error:', err);
});


const Reviews = require('./review');
const Dealerships = require('./dealership');
const Cars = require('./car');

Reviews.deleteMany({}).then(()=>{
  Reviews.insertMany(reviewData['reviews']);
}).catch(error => {
  console.error('Error inserting reviews:', error);
});

Dealerships.deleteMany({}).then(()=>{
  Dealerships.insertMany(dealershipData['dealerships']);
}).catch(error => {
  console.error('Error inserting dealerships:', error);
});

Cars.deleteMany({}).then(()=>{
  Cars.insertMany(carData['cars']);
}).catch(error => {
  console.error('Error inserting cars:', error);
});


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealerships.findOne({ id: req.params.id });
    if (!document) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Express route to fetch all cars
app.get('/fetchCars', async (req, res) => {
  try {
    const documents = await Cars.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching cars' });
  }
});

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0]['id']+1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
