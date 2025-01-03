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
      const response = await fetch(`/djangoapp/fetchReviews/dealer/${id}`);
      const data = await response.json();
      
      if (data.status === 200) {
        setReviews(data.reviews || []);
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
        <h1>{dealer.full_name || dealer.name}</h1>
        <div className="dealer-info mb-4">
          <p>
            {dealer.address && (
              <span>{dealer.address}, </span>
            )}
            {dealer.city && (
              <span>{dealer.city}, </span>
            )}
            {dealer.state && (
              <span>{dealer.state} </span>
            )}
            {dealer.zip && (
              <span>({dealer.zip})</span>
            )}
          </p>
        </div>

        <div className="reviews-section">
          <h2>Reviews</h2>
          {reviews.length > 0 ? (
            <div className="reviews-list">
              {reviews.map((review, index) => (
                <div key={index} className="review-card">
                  <p className="review-text">{review.review}</p>
                  <div className="review-meta">
                    <span>By: {review.name}</span>
                    {review.car_make && (
                      <span> | Car: {review.car_make} {review.car_model} {review.car_year}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>No reviews yet</p>
          )}
        </div>

        {sessionStorage.getItem('username') && (
          <div className="mt-4">
            <Link to={`/dealer/${id}/review`} className="btn btn-primary">
              Write a Review
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dealer;
