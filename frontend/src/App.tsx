import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import TripDetails from "./pages/TripDetails";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trip/:id" element={<TripDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
