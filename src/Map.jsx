import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import './styling/Donor.css';

// Function to get geolocation from address using Nominatim
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

export default function Map() {
  const [donors, setDonors] = useState([]);
  const [coordinates, setCoordinates] = useState([]);

  useEffect(() => {
    fetch('http://localhost:3001/donors')
      .then(response => response.json())
      .then(async (data) => {
        setDonors(data);

        // Fetch coordinates for each donor
        const locations = await Promise.all(
          data.map(async (donor) => {
            return getCoordinates(donor.address);
          })
        );

        // @ts-ignore
        setCoordinates(locations.filter(Boolean)); // Remove null values
      })
      .catch(error => console.error('Error fetching donors:', error));
  }, []);

  return (
    <MapContainer center={[34.054, -118.24]} zoom={12} style={{ height: '500px', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {donors.map((donor, index) => {
        const coord = coordinates[index];

        if (!coord) return null;

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
              address}</strong><br /><br />
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
