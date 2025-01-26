import './style.css';
import './components/Header/Header.css';
import React, { useState, useEffect } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import RegisterPanel from './components/Register/Register';
import Dealer from './components/Dealers/Dealer';
import PostReview from './components/Dealers/PostReview';
import Header from './components/Header/Header';

function Dealers() {
  const [dealers, setDealers] = useState([]);
  const [cars, setCars] = useState([]);
  
  useEffect(() => {
    // Fetch dealers
    fetch('http://localhost:3030/fetchDealers')
      .then(response => response.json())
      .then(data => setDealers(data))
      .catch(error => console.error('Error fetching dealers:', error));

    // Fetch cars  
    fetch('http://localhost:3030/fetchCars')
      .then(response => response.json())
      .then(data => setCars(data))
      .catch(error => console.error('Error fetching cars:', error));
  }, []);

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Dealers and Inventory</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Dealer Name</th>
              <th>Location</th>
              <th>Available Cars</th>
            </tr>
          </thead>
          <tbody>
            {dealers.map(dealer => (
              <tr key={dealer.id}>
                <td>{dealer.full_name}</td>
                <td>{dealer.city}, {dealer.state}</td>
                <td>
                  {cars
                    .filter(car => car.dealer_id === dealer.id)
                    .map(car => (
                      <div key={car._id}>
                        {car.year} {car.make} {car.model}
                      </div>
                    ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Add these components for About and Contact pages
const About = () => (
  <div>
    <Header />
    <div className="container mt-4">
      <h2>About Us</h2>
      <p>Welcome to our car dealership platform.</p>
    </div>
  </div>
);

const Contact = () => (
  <div>
    <Header />
    <div className="container mt-4">
      <h2>Contact Us</h2>
      <p>Get in touch with us.</p>
    </div>
  </div>
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <Dealers />
  },
  {
    path: "/login",
    element: <LoginPanel />
  },
  {
    path: "/register",
    element: <RegisterPanel />
  },
  {
    path: "/dealers",
    element: <Dealers />
  },
  {
    path: "/dealer/:id",
    element: <Dealer />
  },
  {
    path: "/postreview/:id",
    element: <PostReview />
  },
  {
    path: "/about",
    element: <About />
  },
  {
    path: "/contact",
    element: <Contact />
  }
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
