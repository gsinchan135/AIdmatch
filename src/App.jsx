import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css'
import './styling/colors.css'
import 'leaflet/dist/leaflet.css';


import React from 'react'

import Home from './Home.jsx'
import Navbar from './Navbar.jsx';
import Donor from './Donor.jsx';
import Victims from './Victims.jsx';
import Map from './Map.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <Navbar/>
      <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/donors" element={<Donor/>}/>
        <Route path="/victims" element={<Victims/>}/>
        <Route path="/map" element={<Map/>}/>
        <Route path="/public-services" element={<Home/>}/>

      </Routes>
    </Router>
    </div>
  )
}

export default App
