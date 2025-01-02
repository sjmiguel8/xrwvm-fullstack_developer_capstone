import React, { useState, useEffect } from 'react';
import './Dealers.css';

function Dealers() {
  const [dealers, setDealers] = useState([]);

  useEffect(() => {
    fetchDealers();
  }, []);
  
  const fetchDealers = async () => {
    try {
      const response = await fetch('/djangoapp/fetchDealers');
      const data = await response.json();
      setDealers(data);
      console.log('Fetched dealers:', data);  // Debug log
    } catch (error) {
      console.error('Error fetching dealers:', error);
    }
  };

  return (
    <div className="dealers-container">
      <h2>Car Dealers</h2>
      <div className="dealers-list">
        {dealers.map((dealer) => (
          <div key={dealer.id} className="dealer-card">
            <h3>{dealer.name}</h3>
            <p>{dealer.address}</p>
            <p>{dealer.city}, {dealer.state} {dealer.zip_code}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dealers;
