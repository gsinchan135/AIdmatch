import React from 'react';
import './styling/Hero.css'


export default function Hero({imageUrl,text}) {
  return (
    <div className="HeroImage">
      <img src={imageUrl} alt="Hero" className="HeroImage-img" />
      <div className="HeroImage-text">{text}</div>
    </div>
  );
}