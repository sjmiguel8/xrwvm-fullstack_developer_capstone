import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from '../Header/Header';
import './Dealers.css';

function Dealers() {
  const [dealers, setDealers] = useState([]);
  const [filteredDealers, setFilteredDealers] = useState([]);
  const [filterType, setFilterType] = useState('none');
  const [filterValue, setFilterValue] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://staging.d2gtyto3nyfjvh.amplifyapp.com/djangoapp/get_dealers/')
      .then(response => response.json())
      .then(data => {
        setDealers(data);
        setLoading(false);
      })
      .catch(error => {
        setError('Error: ' + error.message);
        console.error('Error:', error);
        setLoading(false);
      });
  }, [error]);

  const handleFilterChange = (type, value) => {
    setFilterType(type);
    setFilterValue(value);

    if (type === 'none' || !value) {
      setFilteredDealers(dealers);
      return;
    }

    const filtered = dealers.filter(dealer => {
      switch (type) {
        case 'state':
          return dealer.state === value;
        case 'city':
          return dealer.city === value;
        case 'name':
          return dealer.name === value;
        case 'id':
          return dealer.id === parseInt(value);
        default:
          return true;
      }
    });
    setFilteredDealers(filtered);
  };

  return (
    <div>
      <Header />
      <div className="dealers-container">
        <h2>Car Dealers</h2>
        
        {error && <div className="alert alert-danger">{error}</div>}
        {loading ? (
          <div>Loading dealers...</div>
        ) : (
          <>
            <div className="filters">
              <div className="row mb-3">
                <div className="col-md-4">
                  <select 
                    className="form-select"
                    value={filterType}
                    onChange={(e) => handleFilterChange(e.target.value, '')}
                  >
                    <option value="none">Filter By...</option>
                    <option value="state">State</option>
                    <option value="city">City</option>
                    <option value="name">Dealer Name</option>
                    <option value="id">ID</option>
                  </select>
                </div>
                {filterType !== 'none' && (
                  <div className="col-md-4">
                    <select
                      className="form-select"
                      value={filterValue}
                      onChange={(e) => handleFilterChange(filterType, e.target.value)}
                    >
                      <option value="">Select {filterType}...</option>
                      {filterType === 'state' && [...new Set(dealers.map(d => d.state))].map(state => (
                        <option key={state} value={state}>{state}</option>
                      ))}
                      {filterType === 'city' && [...new Set(dealers.map(d => d.city))].map(city => (
                        <option key={city} value={city}>{city}</option>
                      ))}
                      {filterType === 'name' && [...new Set(dealers.map(d => d.name))].map(name => (
                        <option key={name} value={name}>{name}</option>
                      ))}
                      {filterType === 'id' && [...new Set(dealers.map(d => d.id))].map(id => (
                        <option key={id} value={id}>{id}</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>
            </div>

            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Dealer Name</th>
                  <th>Short Name</th>
                  <th>City</th>
                  <th>State</th>
                  <th>Address</th>
                  <th>Zip</th>
                  <th>Location</th>
                </tr>
              </thead>
              <tbody>
                {dealers.length > 0 ? (
                  (filterType === 'none' ? dealers : filteredDealers).map((dealer) => (
                    <tr key={dealer.id}>
                      <td>{dealer.id}</td>
                      <td>
                        <Link to={`/dealer/${dealer.id}`}>{dealer.name}</Link>
                      </td>
                      <td>{dealer.short_name}</td>
                      <td>{dealer.city}</td>
                      <td>{dealer.state} ({dealer.st})</td>
                      <td>{dealer.address}</td>
                      <td>{dealer.zip}</td>
                      <td>
                        <a 
                          href={`https://maps.google.com/?q=${dealer.lat},${dealer.long}`}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          Map
                        </a>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="8" className="text-center">No dealers found</td>
                  </tr>
                )}
              </tbody>
            </table>
          </>
        )}
      </div>
    </div>
  );
}

export default Dealers;
