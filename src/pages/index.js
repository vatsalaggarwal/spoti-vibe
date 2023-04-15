import { useState } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  Box,
  Slider,
  TextField,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button,
} from "@mui/material";

const Index = () => {
  // State for form inputs
  const [limit, setLimit] = useState(20);
  const [seedGenres, setSeedGenres] = useState([]);
  const [targetDanceability, setTargetDanceability] = useState(0.5);
  const [targetEnergy, setTargetEnergy] = useState(0.5);

  // State for recommendations
  const [recommendations, setRecommendations] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const params = {
      limit,
      seed_genres: seedGenres.join(","),
      target_danceability: targetDanceability,
      target_energy: targetEnergy,
      // Add other parameters here
    };

    const { data } = await axios.get("/api/recommendations", { params });
    setRecommendations(data.tracks);
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Spotify Recommendations
      </Typography>

      <Box component="form" onSubmit={handleSubmit}>
        <Typography variant="h6">Limit</Typography>
        <TextField
          type="number"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
          fullWidth
        />

        <Typography variant="h6">Seed Genres</Typography>
        <FormControl fullWidth>
          <InputLabel>Genres</InputLabel>
          <Select
            multiple
            value={seedGenres}
            onChange={(e) => setSeedGenres(e.target.value)}
          >
            {/* Add genres as MenuItems here */}
            <MenuItem value={"pop"}>Pop</MenuItem>
            <MenuItem value={"rock"}>Rock</MenuItem>
            <MenuItem value={"hip-hop"}>Hip-Hop</MenuItem>
            <MenuItem value={"jazz"}>Jazz</MenuItem>
            <MenuItem value={"classical"}>Classical</MenuItem>
          </Select>
        </FormControl>

        <Typography variant="h6">Target Danceability</Typography>
        <Slider
          value={targetDanceability}
          onChange={(e, value) => setTargetDanceability(value)}
        />

        <Typography variant="h6">Target Energy</Typography>
        <Slider
          value={targetEnergy}
          onChange={(e, value) => setTargetEnergy(value)}
        />

        {/* Add other components for different parameters here */}

        <Button type="submit" variant="contained" color="primary">
          Get Recommendations
        </Button>
      </Box>

      {/* Display recommendations */}
      <Box my={4}>
        <Typography variant="h6">Recommendations:</Typography>
        <ul>
          {recommendations.map((track) => (
            <li key={track.id}>
              {track.name} - {track.artists[0].name}
            </li>
          ))}
        </ul>
      </Box>
    </Container>
  );
};

export default Index;
