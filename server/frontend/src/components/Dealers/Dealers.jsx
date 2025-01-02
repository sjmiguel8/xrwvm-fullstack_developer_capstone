import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from '../Header/Header';
import './Dealers.css';

function Dealers() {
  // State management
  const [dealers, setDealers] = useState([]);
  const [filteredDealers, setFilteredDealers] = useState([]);
  const [filterType, setFilterType] = useState('none');
  const [filterValue, setFilterValue] = useState('');

  useEffect(() => {
    fetchDealers();
  }, []);

  useEffect(() => {
    filterDealers();
  }, [filterType, filterValue, dealers]);

  const fetchDealers = async () => {
    try {
      const response = await fetch('/djangoapp/fetchDealers');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      if (Array.isArray(data)) {
        setDealers(data);
        setFilteredDealers(data);
      } else {
        console.error('Unexpected data format:', data);
      }
    } catch (error) {
      console.error('Error fetching dealers:', error);
    }
  };

  const filterDealers = () => {
    if (filterType === 'none' || !filterValue) {
      setFilteredDealers(dealers);
      return;
    }

    let filtered = dealers.filter(dealer => {
      switch (filterType) {
        case 'state':
          return dealer.state === filterValue;
        case 'city':
          return dealer.city.toLowerCase().includes(filterValue.toLowerCase());
        case 'id':
          return dealer.id === Number(filterValue);
        case 'name':
          return dealer.name.toLowerCase().includes(filterValue.toLowerCase());
        default:
          return true;
      }
    });
    
    setFilteredDealers(filtered);
  };

  // Get unique values for filters
  const states = [...new Set(dealers.map(dealer => dealer.state))];
  const cities = [...new Set(dealers.map(dealer => dealer.city))];
  const names = [...new Set(dealers.map(dealer => dealer.name))];
  const ids = [...new Set(dealers.map(dealer => dealer.id))];

  return (
    <div>
      <Header />
      <div className="dealers-container">
        <h2>Car Dealers</h2>
        
        <div className="filters">
          <div className="row mb-3">
            <div className="col-md-4">
              <select 
                className="form-select"
                value={filterType}
                onChange={(e) => {
                  setFilterType(e.target.value);
                  setFilterValue('');
                }}
              >
                <option value="none">Filter By...</option>
                <option value="state">State</option>
                <option value="city">City</option>
                <option value="name">Dealer Name</option>
                <option value="id">ID</option>
              </select>
            </div>
            <div className="col-md-4">
              {filterType !== 'none' && (
                <select
                  className="form-select"
                  value={filterValue}
                  onChange={(e) => setFilterValue(e.target.value)}
                >
                  <option value="">Select {filterType}...</option>
                  {filterType === 'state' && states.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                  {filterType === 'city' && cities.map(city => (
                    <option key={city} value={city}>{city}</option>
                  ))}
                  {filterType === 'name' && names.map(name => (
                    <option key={name} value={name}>{name}</option>
                  ))}
                  {filterType === 'id' && ids.map(id => (
                    <option key={id} value={id}>{id}</option>
                  ))}
                </select>
              )}
            </div>
          </div>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Dealer Name</th>
              <th>City</th>
              <th>Address</th>
              <th>Zip</th>
              <th>State</th>
            </tr>
          </thead>
          <tbody>
            {filteredDealers.map((dealer) => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td>
                  <Link to={`/dealer/${dealer.id}`}>{dealer.name}</Link>
                </td>
                <td>{dealer.city}</td>
                <td>{dealer.address}</td>
                <td>{dealer.zip_code}</td>
                <td>{dealer.state}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dealers;
