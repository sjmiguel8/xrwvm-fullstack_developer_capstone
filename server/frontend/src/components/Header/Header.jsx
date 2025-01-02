import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: 'darkturquoise' }}>
      <div className="container-fluid">
        <h2 className="navbar-brand mb-0" style={{ fontSize: '24px', marginRight: '3rem' }}>Dealerships</h2>
        <button 
          className="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link className="nav-link nav-item-custom" to="/">Home</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link nav-item-custom" to="/about">About Us</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link nav-item-custom" to="/contact">Contact Us</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Header;
