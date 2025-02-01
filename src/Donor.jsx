import React, { useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import "./styling/Donor.css"

export default function Donor() {

    const [name, setName] = useState('');
    const [location, setLocation] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [capacity, setCapacity] = useState('');

    const [error, setError] = useState('');

    const nameRef = useRef(null);
    const locationRef = useRef(null);
    const phoneNumberRef = useRef(null);
    const capacityRef = useRef(null);
    const confirmRef = useRef(null);
    
    const handleSubmit = () =>{

    }

    
    const handleContainerClick = (ref) => {
        ref.current?.focus();
    };

    return (
        <form onSubmit={handleSubmit} className="signup-form">

            <div className='form-group'>
            <label>Name:</label>
                <div className="input-wrapper" onClick={() => handleContainerClick(nameRef)}>
                    <span className="input-icon">👤</span>
                    <input className='form-input' 
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
                    <span className="input-icon">🔒</span>
                    <input className='form-input'
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
                    <span className="input-icon">🔒</span>
                    <input className='form-input'
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
                    <span className="input-icon">🔒</span>
                    <input className='form-input'
                        ref={capacityRef} 
                        type="number" 
                        value={capacity} 
                        onChange={(e) => setCapacity(e.target.value)}
                        placeholder='Capacity'
                        required
                    />
                </div>
            </div>
            
            

            <div className='form-actions'>
                <button type="submit" id="confirm-signup">Confirm</button>
                <Link to='/victims' className='form-prompt'>looking for help?</Link>
            </div>
        </form>
    );
}