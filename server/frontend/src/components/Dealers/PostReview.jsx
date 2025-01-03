import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const navigate = useNavigate();

  const { id } = useParams();

  useEffect(() => {
    // Check if user is logged in
    if (!sessionStorage.getItem('username')) {
      navigate('/login');
    }
  }, [navigate]);

  const postreview = async () => {
    if (!review || !date) {
      alert("Please provide both a review and purchase date");
      return;
    }

    const reviewData = {
      name: sessionStorage.getItem("username"),
      dealership: id,
      review: review,
      purchase: true,
      purchase_date: date,
      car_make: model ? model.split(" ")[0] : "",
      car_model: model ? model.split(" ")[1] : "",
      car_year: year || "",
    };

    console.log('Sending review data:', reviewData);

    try {
      const response = await fetch('/djangoapp/add_review', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reviewData)
      });

      const data = await response.json();
      console.log('Review submission response:', data);
      
      if (data.status === 200) {
        navigate(`/dealer/${id}`);
      } else {
        alert('Failed to post review: ' + (data.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error posting review:', error);
      alert('Failed to post review');
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch dealer info
        const dealerRes = await fetch(`/djangoapp/dealer/${id}`);
        const dealerData = await dealerRes.json();
        if (dealerData.status === 200 && dealerData.dealer?.length > 0) {
          setDealer(dealerData.dealer[0]);
        }

        // Fetch car models
        const carsRes = await fetch('/djangoapp/get_cars');
        const carsData = await carsRes.json();
        if (carsData.CarModels) {
          setCarmodels(carsData.CarModels);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [id]);

  return (
    <div>
      <Header />
      <div className="container mt-4">
        <h1 className="mb-4">{dealer.full_name}</h1>
        <div className="mb-3">
          <label className="form-label">Your Review *</label>
          <textarea 
            className="form-control"
            rows="5"
            value={review}
            onChange={(e) => setReview(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Purchase Date *</label>
          <input 
            type="date"
            className="form-control"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Car Make and Model (Optional)</label>
          <select 
            className="form-select"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="">Choose Car Make and Model</option>
            {carmodels.map((car, index) => (
              <option key={index} value={`${car.CarMake} ${car.CarModel}`}>
                {car.CarMake} {car.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Car Year (Optional)</label>
          <input 
            type="number"
            className="form-control"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            min="2015"
            max="2024"
          />
        </div>

        <button 
          className="btn btn-primary"
          onClick={postreview}
        >
          Post Review
        </button>
      </div>
    </div>
  );
};

export default PostReview;
