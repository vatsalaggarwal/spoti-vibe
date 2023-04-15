import axios from "axios";

// Replace the values below with your own credentials
const clientId = "a8dc3eb526834ead97222e34d4f16993";
const clientSecret = "4032b826da664d3b99f918a50f4afeaf";
const base64Credentials = Buffer.from(`${clientId}:${clientSecret}`).toString("base64");

// Function to get an access token from Spotify
const getAccessToken = async () => {
  try {
    const response = await axios.post("https://accounts.spotify.com/api/token", null, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": `Basic ${base64Credentials}`,
      },
      params: {
        "grant_type": "client_credentials",
      },
    });
    return response.data.access_token;
  } catch (error) {
    console.error("Error getting access token:", error);
    return null;
  }
};

// Function to get recommendations from Spotify
const getRecommendations = async (accessToken, params) => {
    console.log(accessToken);
    console.log(params);
  try {
    const response = await axios.get("https://api.spotify.com/v1/recommendations", {
      headers: {
        "Authorization": `Bearer ${accessToken}`,
      },
      params,
    });
    return response.data;
  } catch (error) {
    console.error("Error getting recommendations:", error);
    return null;
  }
};

export default async (req, res) => {
  if (req.method === "GET") {
    const accessToken = await getAccessToken();

    if (!accessToken) {
      res.status(500).json({ error: "Failed to get access token." });
      return;
    }

    // Extract the parameters from the request
    const params = {
        limit: req.query.limit || 20,
        // Add other query parameters here
        target_energy: req.query.target_energy || 0.5,
        target_danceability: req.query.target_danceability || 0.5,
        // seed_artists: req.query.seed_artists || "4NHQUGzhtTLFvgF5SZesLK",
        seed_genres: req.query.seed_genres || "classical,country",
        // seed_tracks: req.query.seed_tracks || "0c6xIDDpzE81m2q797ordA"
    };

    const recommendations = await getRecommendations(accessToken, params);

    if (!recommendations) {
      res.status(500).json({ error: "Failed to get recommendations." });
      return;
    }

    res.status(200).json(recommendations);
  } else {
    res.setHeader("Allow", "GET");
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
};
