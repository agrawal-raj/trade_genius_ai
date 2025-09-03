
import './App.css';
import React from 'react'
// import { Provider } from 'react-redux'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
// import { store } from './store'
import HomePage from './pages/HomePage'
import CompanyPage from './pages/CompanyPage'


function App() {
  return (
      <Router>
        <div className= "App">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/company/:companyId" element={<CompanyPage />} />
            </Routes>
          </div>
      </Router>
  );
}

export default App;
