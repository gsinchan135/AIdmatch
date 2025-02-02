import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Matchup = () => {
    const [donors, setDonors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDonors = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/get_top_donors');
                setDonors(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchDonors();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h1>Top Donors</h1>
            <ul>
                {donors.map((donor, index) => (
                    <li key={index}>{donor.name} - ${donor.}</li>
                ))}
            </ul>
        </div>
    );
};

export default Matchup;