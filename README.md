# Trip Management System

## 📌 Overview

The **Trip Management System** is a web-based application designed to manage trips, calculate estimated distances and times using OpenRouteService, display routes on an interactive map, and generate trip reports in PDF format.

## 🚀 Features

- **Create, View, Delete Trips**
- **Calculate Distance & Time** using OpenRouteService API
- **Display Routes on a Map** (Leaflet + OpenStreetMap)
- **Generate Trip Reports in PDF**
- **Responsive UI with Material UI**

## 🛠️ Tech Stack

- **Frontend:** React, TypeScript, Material UI, Leaflet
- **Backend:** Django, Django REST Framework (DRF), OpenRouteService API
- **Database:** PostgreSQL (or SQLite for testing)
- **API Calls:** Fetch API, Axios

---

## 📂 Project Structure

```
trip-management/
│── frontend/         # React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.tsx
│   │   ├── index.tsx
│   ├── package.json
│── backend/          # Django Backend
│   ├── trips/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   ├── manage.py
│   ├── requirements.txt
│── README.md
```

---

## ⚡ Setup & Installation

### **Backend Setup** (Django)

1. **Create Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate  # For Windows
   ```
2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run Migrations & Start Server**
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```
4. **Test API (Optional)**
   ```sh
   python manage.py test
   ```

### **Frontend Setup** (React + TypeScript)

1. **Navigate to Frontend Directory**
   ```sh
   cd frontend
   ```
2. **Install Dependencies**
   ```sh
   npm install
   ```
3. **Start Development Server**
   ```sh
   npm start
   ```
4. **Access Application** Open `http://localhost:5173` in your browser.

---

## 🔑 API Configuration

### OpenRouteService API Key

- Add your **OpenRouteService API Key** to `.env` (for backend) and `api.ts` (for frontend):
  ```env
  OPENROUTE_API_KEY=your_api_key_here
  ```

### Backend API Endpoints

| Method   | Endpoint               | Description         |
| -------- | ---------------------- | ------------------- |
| `GET`    | `/api/trips/`          | List all trips      |
| `POST`   | `/api/trips/`          | Create a new trip   |
| `GET`    | `/api/trips/{id}/`     | Get trip details    |
| `DELETE` | `/api/trips/{id}/`     | Delete a trip       |
| `GET`    | `/api/trips/{id}/pdf/` | Generate PDF report |

---

## 🗺️ Map & Route Visualization

- Uses **Leaflet.js** with **OpenStreetMap** as tile provider.
- Route data is fetched using **OpenRouteService** API.

---

## 📝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-xyz`
3. Commit your changes: `git commit -m "Added new feature"`
4. Push to the branch: `git push origin feature-xyz`
5. Submit a Pull Request

---

