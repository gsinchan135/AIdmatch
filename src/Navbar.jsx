import React from 'react';
import './styling/Navbar.css'; 

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <a href="/" className="website-name">AIdmatch</a>
      </div> 
      <ul className="navbar-links">
        <li><a href="/" className="nav-link">Home</a></li>
        <li><a href="/donors" className="nav-link">Donors</a></li>
        <li><a href="/victims" className="nav-link">Victims</a></li>
        <li><a href="/public-services" className="nav-link">Public Services</a></li>
      </ul>
    </nav>
  );
};

