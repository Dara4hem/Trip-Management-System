import { useState } from "react";
import { Container, Typography, Paper, Divider, Grid, Tabs, Tab } from "@mui/material";
import TripForm from "../components/TripForm";
import TripList from "../components/TripList";

const Dashboard = () => {
  const [reload, setReload] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  return (
    <Container maxWidth="lg">
      <Paper elevation={6} sx={{ p: 5, mt: 5, borderRadius: 3, backgroundColor: "#f8f9fa" }}>
        <Typography variant="h3" gutterBottom align="center" color="primary" fontWeight="bold">
          🚀 Trip Management System
        </Typography>
        <Typography variant="subtitle1" align="center" color="textSecondary">
          Plan, track, and manage your trips effortlessly.
        </Typography>

        <Divider sx={{ my: 4 }} />

        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)} centered>
          <Tab label="Create a Trip" />
          <Tab label="View Trips" />
        </Tabs>

        <Divider sx={{ my: 2 }} />

        <Grid container spacing={4} justifyContent="center">
          <Grid item xs={12} md={8} sx={{ display: tabValue === 0 ? "block" : "none" }}>
            <TripForm onTripCreated={() => setReload(!reload)} />
          </Grid>
          <Grid item xs={12} md={10} sx={{ display: tabValue === 1 ? "block" : "none" }}>
            <TripList key={reload.toString()} />
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default Dashboard;
