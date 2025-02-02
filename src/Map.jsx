import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
// @ts-ignore
// @ts-ignore
import axios from 'axios';
import 'leaflet/dist/leaflet.css'; 
import './styling/Donor.css'; 

// Function to generate random coordinates within a specified radius
function generateRandomCoordinates(centerLat, centerLon, radiusKm) {
  const radiusInDegrees = radiusKm / 111.32;

  const randomLat = centerLat + (Math.random() - 0.5) * 2 * radiusInDegrees;
  const randomLon = centerLon + (Math.random() - 0.5) * 2 * radiusInDegrees / Math.cos(centerLat * Math.PI / 180);

  return {
    lat: randomLat,
    lon: randomLon
  };
}

const LAlat = 34.0522;
const LAlon = -118.2437;  

export default function Map() {
  const [donors, setDonors] = useState([]);
  const [coordinates, setCoordinates] = useState([]);  // Store coordinates for each donor

  useEffect(() => {
    fetch('http://localhost:3001/donors')  
      .then(response => response.json())
      .then((data) => {
        setDonors(data);

        // Generate random coordinates for each donor
        const randomCoordinates = data.map(() => generateRandomCoordinates(LAlat, LAlon, 50));
        setCoordinates(randomCoordinates);
      })
      .catch(error => console.error("Error fetching donors:", error));
  }, []);

  return (
    <MapContainer center={[34.054, -118.24]} zoom={12} style={{ height: "500px", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      
      {donors.map((donor, index) => {
        const coord = coordinates[index];

        if (!coord) return null; // Skip rendering if no coordinates are available

        return (
          <Marker 
            key={index} 
            position={[coord.lat, coord.lon]} 
            icon={L.icon({ iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png' })}
          >
            <Popup>
              <strong>{donor.
            // @ts-ignore
              name}</strong><br />
              <strong>{donor.
            // @ts-ignore
            location}</strong>
              <br />
              <br/>
              Phone: {donor.
            // @ts-ignore
              phoneNumber}<br />
              Capacity: {donor.
// @ts-ignore
              capacity}
              <br/>
              {donor.
            // @ts-ignore
              description}
              <br />
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
