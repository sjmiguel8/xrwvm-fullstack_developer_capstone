import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import Dealers from './components/Dealers/Dealers';
import Dealer from './components/Dealers/Dealer';
import Header from './components/Header/Header';

// Simple components for About and Contact
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
    element: <Dealers />,
  },
  {
    path: "/login",
    element: <LoginPanel />,
  },
  {
    path: "/dealers",
    element: <Dealers />,
  },
  {
    path: "/dealer/:id",
    element: <Dealer />,
  },
  {
    path: "/about",
    element: <About />,
  },
  {
    path: "/contact",
    element: <Contact />,
  }
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
