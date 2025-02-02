import React, { useEffect, useState } from 'react';
import './styling/Victims.css';

const Victims = () => {
  const [donors, setDonors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [donorsPerPage] = useState(20);
  const [victimMessage, setVictimMessage] = useState('');
  const [topDonors, setTopDonors] = useState([]);

  useEffect(() => {
    const fetchDonors = async () => {
      const response = await fetch('http://localhost:5000/donors');
      const data = await response.json();
      setDonors(data);
    };

    fetchDonors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/get_top_donors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ victim_text: victimMessage, victim_location: { latitude: 40.7128, longitude: -74.0060 } })
      });
      const result = await response.json();
      if (response.ok) {
        setTopDonors(result.top_donors);
      } else {
        console.error("Error:", result.error);
      }
    } catch (err) {
      console.error("Failed to fetch top donors:", err);
    }
  };

  const indexOfLastDonor = currentPage * donorsPerPage;
  const indexOfFirstDonor = indexOfLastDonor - donorsPerPage;
  const currentDonors = donors.slice(indexOfFirstDonor, indexOfLastDonor);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="victims-container">
      <h1>Help</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={victimMessage}
          onChange={(e) => setVictimMessage(e.target.value)}
          placeholder="Describe your situation..."
          required
        />
        <button type="submit">Find Help</button>
      </form>
      {topDonors.length > 0 && (
        <div className="top-donors">
          <h2>Top Donors</h2>
          <ul>
            {topDonors.map((donor, index) => (
              <li key={index}>
                <p><strong>ID:</strong> {donor.id}</p>
                <p><strong>Score:</strong> {donor.score}</p>
                <p><strong>Distance:</strong> {donor.distance} km</p>
                <p><strong>Offer Summary:</strong> {donor.offer_summary}</p>
                <p><strong>Remaining Capacity:</strong> {donor.capacity}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
      <table className="donor-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Phone Number</th>
            <th>Capacity</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {currentDonors.map((donor, index) => (
            <tr key={index}>
              <td>{donor.name}</td>
              <td>{donor.location}</td>
              <td>{donor.phoneNumber}</td>
              <td>{donor.capacity}</td>
              <td>{donor.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        {Array.from({ length: Math.ceil(donors.length / donorsPerPage) }, (_, index) => (
          <button key={index + 1} onClick={() => paginate(index + 1)} className={currentPage === index + 1 ? 'active' : ''}>
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Victims;