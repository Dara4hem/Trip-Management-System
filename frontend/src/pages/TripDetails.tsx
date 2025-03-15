import { useEffect, useState, useMemo } from "react";
import { useParams } from "react-router-dom";
import { getTripDetails } from "../services/api";
import { Container, Typography, Paper, Grid, Button, CircularProgress, Alert } from "@mui/material";
import { MapContainer, Marker, Polyline, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { LatLngExpression } from "leaflet";

const OPENROUTE_API_KEY = "5b3ce3597851110001cf624837c701f22636484b8007e1f141bda9ef";

const TripDetails = () => {
  const { id } = useParams();
  const [trip, setTrip] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [route, setRoute] = useState<LatLngExpression[]>([]);
  const [mapLoading, setMapLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [estimatedTime, setEstimatedTime] = useState<string>("Calculating...");
  const [estimatedDistance, setEstimatedDistance] = useState<string>("Calculating...");

  useEffect(() => {
    const fetchTrip = async () => {
      try {
        const data = await getTripDetails(Number(id));
        console.log("✅ Trip Data Received:", data);
        setTrip(data.trip);

        // ✅ Ensure estimated time and distance are set properly
        setEstimatedTime(data.estimated_time_hours ? `${data.estimated_time_hours} hours` : "Not Available");
        setEstimatedDistance(data.estimated_distance_km ? `${data.estimated_distance_km} km` : "Not Available");
      } catch (error) {
        console.error("❌ Error fetching trip details:", error);
        setError("Failed to load trip details.");
      } finally {
        setLoading(false);
      }
    };
    fetchTrip();
  }, [id]);

  const origin: LatLngExpression | null = useMemo(() => {
    if (trip?.pickup_latitude && trip?.pickup_longitude) {
      return [trip.pickup_latitude, trip.pickup_longitude];
    }
    return null;
  }, [trip]);

  const destination: LatLngExpression | null = useMemo(() => {
    if (trip?.dropoff_latitude && trip?.dropoff_longitude) {
      return [trip.dropoff_latitude, trip.dropoff_longitude];
    }
    return null;
  }, [trip]);

  useEffect(() => {
    if (origin && destination) {
      setMapLoading(true);
      const fetchRoute = async () => {
        const url = `https://api.openrouteservice.org/v2/directions/driving-car?api_key=${OPENROUTE_API_KEY}&start=${origin[1]},${origin[0]}&end=${destination[1]},${destination[0]}`;
        try {
          const response = await fetch(url);
          const data = await response.json();
          console.log("✅ Route Data:", data);
          if (data.routes && data.routes.length > 0) {
            const coordinates = data.routes[0].geometry.coordinates.map(([lng, lat]: [number, number]) => [lat, lng]);
            setRoute(coordinates);
          }
        } catch (error) {
          console.error("❌ Error fetching route:", error);
        } finally {
          setMapLoading(false);
        }
      };
      fetchRoute();
    }
  }, [origin, destination]);

  const handleExportPDF = () => {
    window.open(`http://127.0.0.1:8000/api/trips/${id}/pdf/`, "_blank");
  };

  if (loading) {
    return (
      <Container sx={{ textAlign: "center", mt: 4 }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading trip details...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ textAlign: "center", mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Paper elevation={4} sx={{ p: 4 }}>
        <Typography variant="h4">🚗 Trip Details</Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" color="secondary">Pickup Location:</Typography>
            <Typography variant="body1">{trip?.pickup_location ?? "Loading..."}</Typography>

            <Typography variant="h6" color="secondary" sx={{ mt: 2 }}>Dropoff Location:</Typography>
            <Typography variant="body1">{trip?.dropoff_location ?? "Loading..."}</Typography>

            <Typography variant="h6" color="secondary" sx={{ mt: 2 }}>Estimated Distance:</Typography>
            <Typography variant="body1">{estimatedDistance}</Typography>

            <Typography variant="h6" color="secondary" sx={{ mt: 2 }}>Estimated Time:</Typography>
            <Typography variant="body1">{estimatedTime}</Typography>

            <Button variant="contained" color="primary" sx={{ mt: 3, mr: 2 }} href="/">
              Back to Dashboard
            </Button>
            <Button variant="contained" color="secondary" sx={{ mt: 3 }} onClick={handleExportPDF}>
              Export as PDF
            </Button>
          </Grid>

          <Grid item xs={12} md={6}>
            {origin && destination && !mapLoading ? (
              <MapContainer center={origin} zoom={10} style={{ height: "400px", width: "100%" }}>
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Marker position={origin} />
                <Marker position={destination} />
                {route.length > 0 && <Polyline pathOptions={{ color: "blue" }} positions={route} />}
              </MapContainer>
            ) : (
              <Typography variant="body2" color="error" align="center">
                🔄 Loading map data...
              </Typography>
            )}
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default TripDetails;
