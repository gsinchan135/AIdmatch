import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './styling/Donor.css';

export default function Map() {
  const [donors, setDonors] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/get_top_donors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ victim_text: "Need urgent help", victim_location: { latitude: 40.7128, longitude: -74.0060 } })
    })
      .then(response => response.json())
      .then(data => {
        setDonors(data);
      })
      .catch(error => console.error('Error fetching donors:', error));
  }, []);

  return (
    <MapContainer center={[34.054, -118.24]} zoom={12} style={{ height: '500px', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {donors.map((donor, index) => {
        // @ts-ignore
        if (!donor.latitude || !donor.longitude) return null; // Ensure coordinates exist

        return (
          <Marker
            key={index}
            // @ts-ignore
            position={[donor.latitude, donor.longitude]}
            icon={L.icon({ iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png' })}
          >
            <Popup>
              <strong>{donor.
// @ts-ignore
              name}</strong><br />
              <strong>{donor.
// @ts-ignore
              location}</strong><br /><br />
              Phone: {donor.
// @ts-ignore
              phoneNumber}<br />
              Capacity: {donor.
// @ts-ignore
              capacity}<br />
              {donor.
// @ts-ignore
              description}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
