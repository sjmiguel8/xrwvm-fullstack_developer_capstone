import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import "./Dealers.css";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();

  const fetchDealer = useCallback(async () => {
    try {
      const response = await fetch(`/djangoapp/dealer/${id}`);
      const data = await response.json();
      
      if (data.status === 200 && data.dealer && data.dealer.length > 0) {
        setDealer(data.dealer[0]);
      } else {
        setError(data.message || 'Failed to load dealer information');
      }
    } catch (error) {
      console.error('Error fetching dealer:', error);
      setError('Error loading dealer information');
    } finally {
      setLoading(false);
    }
  }, [id]);

  const fetchReviews = useCallback(async () => {
    try {
      console.log('Fetching reviews for dealer:', id);
      const response = await fetch(`/djangoapp/fetchReviews/dealer/${id}`);
      const data = await response.json();
      
      console.log('Review data received:', data);
      
      if (data.status === 200) {
        setReviews(data.reviews || []);
        console.log('Reviews set to state:', data.reviews);
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  }, [id]);

  useEffect(() => {
    fetchDealer();
    fetchReviews();
  }, [fetchDealer, fetchReviews]);

  if (loading) {
    return (
      <div>
        <Header />
        <div className="container mt-4">
          <p>Loading dealer information...</p>
        </div>
      </div>
    );
  }

  if (error || !dealer) {
    return (
      <div>
        <Header />
        <div className="container mt-4">
          <div className="alert alert-danger">
            {error || 'Dealer not found'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      <div className="container mt-4">
        <div className="dealer-details-card">
          <h1 className="dealer-title">{dealer.full_name || dealer.name}</h1>
          <div className="dealer-info">
            <div className="location-info">
              <i className="fas fa-map-marker-alt location-icon"></i>
              <div className="address-details">
                {dealer.address && (
                  <span className="address-line">{dealer.address}</span>
                )}
                <span className="city-state">
                  {dealer.city && <span>{dealer.city}, </span>}
                  {dealer.state && <span>{dealer.state} </span>}
                  {dealer.zip && <span className="zip-code">({dealer.zip})</span>}
                </span>
              </div>
            </div>
          </div>

          <div className="reviews-section">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>Reviews</h2>
              {sessionStorage.getItem('username') ? (
                <Link 
                  to={`/postreview/${id}`} 
                  className="btn btn-primary"
                >
                  Write a Review
                </Link>
              ) : (
                <Link 
                  to="/login" 
                  className="btn btn-outline-primary"
                >
                  Login to Write a Review
                </Link>
              )}
            </div>

            {reviews.length > 0 ? (
              <div className="reviews-list">
                {reviews.map((review, index) => (
                  <div key={index} className="review-card">
                    <p className="review-text">{review.review}</p>
                    <div className="review-meta">
                      <span className="reviewer-name">By: {review.name}</span>
                      {review.car_make && review.car_model && (
                        <span className="car-info">
                          | Car: {review.car_make} {review.car_model} 
                          {review.car_year && ` ${review.car_year}`}
                        </span>
                      )}
                      {review.purchase_date && (
                        <span className="review-date">
                          | Purchased: {new Date(review.purchase_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>No reviews yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dealer;
