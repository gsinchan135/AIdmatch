import React, { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import "./styling/Donor.css";
import axios from 'axios';


export default function Donor() {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [capacity, setCapacity] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const nameRef = useRef(null);
  const locationRef = useRef(null);
  const phoneNumberRef = useRef(null);
  const capacityRef = useRef(null);
  const descRef = useRef(null);

  const getCoordinates = async (address) => {
    try {
      const NOMINATIM_BASE_URL = 'https://nominatim.openstreetmap.org/search';
      // @ts-ignore
      const params = new URLSearchParams({
        q: address,
        format: 'json',
        limit: 1,
      });
  
      const response = await axios.get(`${NOMINATIM_BASE_URL}?${params}`);
      if (response.data.length > 0) {
        return {
          lat: parseFloat(response.data[0].lat),
          lon: parseFloat(response.data[0].lon),
        };
      }
    } catch (error) {
      console.error('Error fetching coordinates:', error);
    }
    return null;
  };

  const handleContainerClick = (ref) => {
    ref.current?.focus();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const donorData = { name, location, phoneNumber, capacity,description };
    try {
      const response = await fetch('http://localhost:3001/donors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(donorData)
      });
      const result = await response.json();
      if (response.ok) {
        console.log(result.message);
      } else {
        setError(result.error || 'An error occurred while saving donor data.');
      }
    } catch (err) {
      setError('Failed to save donor data.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="signup-form">
      <div className='form-group'>
        <label>Name:</label>
        <div className="input-wrapper" onClick={() => handleContainerClick(nameRef)}>
          <span className="input-icon">👤</span>
          <input
            className='form-input'
            ref={nameRef}
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder='Name'
            required
          />
        </div>
      </div>
      <div className='form-group'>
        <label>Location:</label>
        <div className="input-wrapper" onClick={() => handleContainerClick(locationRef)}>
          <span className="input-icon">📍</span>
          <input
            className='form-input'
            ref={locationRef}
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder='Location'
            required
          />
        </div>
      </div>
      <div className='form-group'>
        <label>Phone Number:</label>
        <div className="input-wrapper" onClick={() => handleContainerClick(phoneNumberRef)}>
          <span className="input-icon">📞</span>
          <input
            className='form-input'
            ref={phoneNumberRef}
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder='Phone Number'
            required
          />
        </div>
      </div>
      <div className='form-group'>
        <label>Capacity:</label>
        <div className="input-wrapper" onClick={() => handleContainerClick(capacityRef)}>
          <span className="input-icon">🔢</span>
          <input
            className='form-input'
            ref={capacityRef}
            type="number"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            placeholder='Capacity'
            required
          />
        </div>
      </div>

      <div className='form-group'>
        <label>Description:</label>
        <div className="input-wrapper" onClick={() => handleContainerClick(descRef)}>
          <span className="input-icon"> </span>
          <textarea
            className='form-input'
            id='description-input'
            ref={descRef}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder='Description'
            required
          ></textarea>
        </div>
      </div>

      {error && <p className="error">{error}</p>}
      <div className='form-actions'>
        <button type="submit" id="confirm-signup">Confirm</button>
        <Link to='/victims' className='form-prompt'>looking for help?</Link>
      </div>
    </form>
  );
}
