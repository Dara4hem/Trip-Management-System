import { useState } from "react";
import { createTrip } from "../services/api";
import { TextField, Button, Typography, Container, Paper, Snackbar, Alert } from "@mui/material";

const TripForm = ({ onTripCreated }: { onTripCreated: () => void }) => {
  const [tripData, setTripData] = useState({
    current_location: "",
    pickup_location: "",
    dropoff_location: "",
    current_latitude: null,
    current_longitude: null,
    pickup_latitude: null,
    pickup_longitude: null,
    dropoff_latitude: null,
    dropoff_longitude: null,
  });

  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchCoordinates = async (location: string, fieldPrefix: string) => {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${location}`);
      const data = await response.json();
      if (data.length > 0) {
        const { lat, lon } = data[0];
        setTripData((prevData) => ({
          ...prevData,
          [`${fieldPrefix}_latitude`]: parseFloat(lat),
          [`${fieldPrefix}_longitude`]: parseFloat(lon),
        }));
      } else {
        console.error(`❌ No coordinates found for ${location}`);
      }
    } catch (error) {
      console.error("❌ Error fetching coordinates:", error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setTripData({ ...tripData, [name]: value });

    if (name === "current_location") fetchCoordinates(value, "current");
    if (name === "pickup_location") fetchCoordinates(value, "pickup");
    if (name === "dropoff_location") fetchCoordinates(value, "dropoff");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    if (!tripData.current_latitude || !tripData.dropoff_latitude) {
      console.error("❌ Missing coordinates data!");
      setLoading(false);
      return;
    }

    console.log("🚀 Sending Trip Data:", tripData);
    try {
      await createTrip(tripData);
      onTripCreated();
      setOpenSnackbar(true);
    } catch (error) {
      console.error("❌ Error creating trip:", error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={4} sx={{ p: 4, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom color="primary" fontWeight="bold">
          ✈️ Create a New Trip
        </Typography>
        <form onSubmit={handleSubmit}>
          {["current_location", "pickup_location", "dropoff_location"].map((field) => (
            <TextField
              key={field}
              label={field.replace("_", " ")}
              name={field}
              value={(tripData as any)[field]}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
            />
          ))}

          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }} disabled={loading}>
            {loading ? "Creating..." : "CREATE TRIP"}
          </Button>
        </form>
      </Paper>

      <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
        <Alert severity="success">Trip Created Successfully!</Alert>
      </Snackbar>
    </Container>
  );
};

export default TripForm;
