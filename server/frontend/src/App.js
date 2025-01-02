import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import Dealers from './components/Dealers/Dealers';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealers" element={<Dealers />} />

    </Routes>
  );
}

export default App;
