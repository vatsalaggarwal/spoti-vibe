import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [limit, setLimit] = useState(20);
  // Add other states for each parameter here
  const [recommendations, setRecommendations] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Update the URL with your API endpoint
    const url = "http://localhost:5000/recommendations";
    try {
      const response = await axios.get(url, {
        params: {
          limit: limit,
          // Add other parameters here
        },
      });

      setRecommendations(response.data.tracks);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Limit:
          <input
            type="number"
            min="1"
            max="100"
            value={limit}
            onChange={(e) => setLimit(e.target.value)}
          />
        </label>
        {/* Add input fields for other parameters here */}
        <button type="submit">Get Recommendations</button>
      </form>

      <h2>Recommended Tracks:</h2>
      <ul>
        {recommendations.map((track) => (
          <li key={track.id}>{track.name} - {track.artists[0].name}</li>
        ))}
      </ul>
    </div>
  );
}
