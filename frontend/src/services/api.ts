import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/";

export const createTrip = async (tripData: any) => {
    console.log("🚀 Sending Trip Data:", tripData);
    const response = await axios.post(`${API_BASE_URL}trips/`, tripData);
    console.log("✅ Trip Created:", response.data); 
    return response.data;
  };
  

export const getTrips = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}trips/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching trips:", error);
    throw error;
  }
};



export const getTripDetails = async (tripId: number) => {
  const response = await axios.get(`${API_BASE_URL}trips/${tripId}/`);
  console.log("✅ Trip API Response:", response.data); // ✅ تأكد من أن الوقت يظهر هنا
  return response.data;
};



export const deleteTrip = async (tripId: number) => {
  try {
    await axios.delete(`${API_BASE_URL}trips/${tripId}/`);
  } catch (error) {
    console.error("Error deleting trip:", error);
    throw error;
  }
};
