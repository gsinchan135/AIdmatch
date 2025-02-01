import React, { useState, useEffect } from 'react';
import { GoogleMap, Marker, useLoadScript } from '@react-google-maps/api';

// Map settings
const mapContainerStyle = {
  width: '100%',
  height: '600px',
};

const center = {
  lat: 37.7749, // Default center (San Francisco)
  lng: -122.4194,
};

const MapComponent = () => {
  const [donors, setDonors] = useState([]); // State to store donor data
  const [markers, setMarkers] = useState([]); // State to store map markers
  const { isLoaded, loadError } = useLoadScript({
    // @ts-ignore
    googleMapsApiKey: process.env.MAPS_API_KEY,
  });

  // Fetch donor data from the backend
  useEffect(() => {
    fetch('http://localhost:5000/donors') // Replace with your backend URL
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => setDonors(data))
      .catch((error) => console.error('Error fetching donors:', error));
  }, []);

  // Geocode donor addresses and set markers
  useEffect(() => {
    if (!isLoaded || donors.length === 0) return;

    const geocodeDonors = async () => {
      const newMarkers = [];

      for (const donor of donors) {
        try {
          const response = await fetch(
            `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
              // @ts-ignore
              donor.address
            )}&key=${process.env.MAPS_API_KEY}`
          );
          const data = await response.json();

          if (data.status === 'OK' && data.results.length > 0) {
            const location = data.results[0].geometry.location;
            newMarkers.push({
              // @ts-ignore
              id: donor.name,
              position: { lat: location.lat, lng: location.lng },
              // @ts-ignore
              label: donor.name,
            });
          } else {
            // @ts-ignore
            console.error(`Geocoding failed for address: ${donor.address}`);
          }
        } catch (error) {
          console.error('Error geocoding address:', error);
        }
      }

      // @ts-ignore
      setMarkers(newMarkers);
    };

    geocodeDonors();
  }, [donors, isLoaded]);

  if (loadError) return <div>Error loading maps</div>;
  if (!isLoaded) return <div>Loading Maps...</div>;

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      zoom={4}
      center={center}
    >
      {markers.map((marker) => (
        <Marker
          // @ts-ignore
          key={marker.id}
          // @ts-ignore
          position={marker.position}
          // @ts-ignore
          label={marker.label} // Display the donor name as a label
        />
      ))}
    </GoogleMap>
  );
};

export default MapComponent;