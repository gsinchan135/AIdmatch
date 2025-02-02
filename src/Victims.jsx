import React, { useEffect, useState } from 'react';

import './styling/Victims.css'

const Victims = () => {
  const [donors, setDonors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [donorsPerPage] = useState(20);

  useEffect(() => {
    const fetchDonors = async () => {
      const response = await fetch('http://localhost:3001/donors');
      const data = await response.json();
      setDonors(data);
    };

    fetchDonors();
  }, []);

  const indexOfLastDonor = currentPage * donorsPerPage;
  const indexOfFirstDonor = indexOfLastDonor - donorsPerPage;
  const currentDonors = donors.slice(indexOfFirstDonor, indexOfLastDonor);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="victims-container">
      <h1>Help</h1>
      <textarea id='victim-situation'></textarea>
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
