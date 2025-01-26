import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  const isLoggedIn = sessionStorage.getItem('username');

  const handleLogout = () => {
    sessionStorage.removeItem('username');
    window.location.href = '/';
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: 'rgb(0, 0, 0)' }}>
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
          <ul className="navbar-nav me-auto">
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
          <ul className="navbar-nav">
            {isLoggedIn ? (
              <>
                <li className="nav-item">
                  <span className="nav-link nav-item-custom">Welcome, {isLoggedIn}</span>
                </li>
                <li className="nav-item">
                  <button 
                    className="nav-link nav-item-custom btn btn-link" 
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link nav-item-custom" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link nav-item-custom" to="/register">Register</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Header;
