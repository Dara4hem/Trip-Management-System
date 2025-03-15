import { useEffect, useState } from "react";
import { getTrips, deleteTrip } from "../services/api";
import { Card, CardContent, Typography, Grid, Paper, CircularProgress, IconButton, Snackbar, Alert } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { Link } from "react-router-dom";

interface Trip {
  id: number;
  current_location: string;
  pickup_location: string;
  dropoff_location: string;
}

const TripList = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const data: Trip[] = await getTrips();
        setTrips(data);
      } catch (error) {
        console.error("Error fetching trips:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTrips();
  }, []);

  const handleDelete = async (tripId: number) => {
    if (window.confirm("Are you sure you want to delete this trip?")) {
      try {
        await deleteTrip(tripId);
        setTrips(trips.filter((trip) => trip.id !== tripId));
        setSnackbarMessage("Trip deleted successfully!");
        setOpenSnackbar(true);
      } catch (error) {
        console.error("❌ Error deleting trip:", error);
        setSnackbarMessage("Failed to delete trip.");
        setOpenSnackbar(true);
      }
    }
  };
  

  return (
    <Paper elevation={3} sx={{ p: 3, borderRadius: 2, backgroundColor: "#ffffff" }}>
      <Typography variant="h5" gutterBottom color="primary" fontWeight="bold">
        📌 Trip List
      </Typography>

      {loading ? (
        <CircularProgress color="primary" />
      ) : (
        <Grid container spacing={3}>
          {trips.length > 0 ? (
            trips.map((trip) => (
              <Grid item xs={12} sm={6} md={4} key={trip.id}>
                <Link to={`/trip/${trip.id}`} style={{ textDecoration: "none", color: "inherit" }}>
                  <Card elevation={5} sx={{ cursor: "pointer", borderRadius: 3, "&:hover": { boxShadow: 8, transform: "scale(1.02)", transition: "0.3s" } }}>
                    <CardContent>
                      <Typography variant="h6" color="secondary" fontWeight="bold">
                        {trip.pickup_location} ➝ {trip.dropoff_location}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Current Location: {trip.current_location}
                      </Typography>
                    </CardContent>
                  </Card>
                </Link>
                <IconButton onClick={() => handleDelete(trip.id)} sx={{ color: "red" }}>
                  <DeleteIcon />
                </IconButton>
              </Grid>
            ))
          ) : (
            <Typography variant="body2" color="textSecondary" align="center">
              No trips available.
            </Typography>
          )}
        </Grid>
      )}

      <Snackbar open={openSnackbar} autoHideDuration={3000} onClose={() => setOpenSnackbar(false)}>
        <Alert severity="success">{snackbarMessage}</Alert>
      </Snackbar>
    </Paper>
  );
};

export default TripList;
