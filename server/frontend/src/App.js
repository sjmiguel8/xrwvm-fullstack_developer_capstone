import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import Dealers from './components/Dealers/Dealers';
import Dealer from './components/Dealers/Dealer';
import Header from './components/Header/Header';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dealers />} />
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/dealers" element={<Dealers />} />
        <Route path="/dealer/:id" element={<Dealer />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </Router>
  );
}

// Simple components for About and Contact pages
function About() {
  return (
    <div>
      <Header />
      <div className="container mt-4">
        <h2>About Us</h2>
        <p>Welcome to our car dealership platform.</p>
      </div>
    </div>
  );
}

function Contact() {
  return (
    <div>
      <Header />
      <div className="container mt-4">
        <h2>Contact Us</h2>
        <p>Get in touch with us.</p>
      </div>
    </div>
  );
}

export default App;
