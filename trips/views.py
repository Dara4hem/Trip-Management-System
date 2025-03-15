import requests
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trip, LogEntry
from .serializers import TripSerializer, LogEntrySerializer
from rest_framework import status
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import qrcode
import io
from datetime import datetime
from PIL import Image  
from django.shortcuts import get_object_or_404

class TripPDFView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="trip_{pk}.pdf"'

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        pdf.setFont("Helvetica-Bold", 20)
        pdf.setFillColor(colors.darkblue)
        pdf.drawString(240, height - 50, "Trip Report")

        pdf.setStrokeColor(colors.darkblue)
        pdf.setLineWidth(2)
        pdf.line(50, height - 60, width - 50, height - 60)

        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)
        pdf.drawString(50, height - 90, f"Trip ID: {trip.id}")
        pdf.drawString(50, height - 110, f"Current Location: {trip.current_location}")
        pdf.drawString(50, height - 130, f"Pickup Location: {trip.pickup_location}")
        pdf.drawString(50, height - 150, f"Dropoff Location: {trip.dropoff_location}")
        pdf.drawString(50, height - 170, f"Distance: {trip.cycle_hours_used} km")
        pdf.drawString(50, height - 190, f"Created At: {trip.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


        qr = qrcode.make(f"http://127.0.0.1:8000/api/trips/{trip.id}/")
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        qr_image = Image.open(qr_buffer)
        qr_image_path = "qr_code.png"
        qr_image.save(qr_image_path, format="PNG")  

        pdf.drawInlineImage(qr_image_path, width - 150, height - 200, width=80, height=80)

        logs = trip.logs.all()
        data = [["Date", "Driving Hours", "On Duty", "Off Duty", "Remaining Hours"]]
        for log in logs:
            data.append([
                log.date.strftime('%Y-%m-%d'),
                log.driving_hours,
                log.on_duty_hours,
                log.off_duty_hours,
                log.remaining_hours
            ])

        table = Table(data, colWidths=[100, 90, 80, 80, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 50, height - 320)

        pdf.setFont("Helvetica-Oblique", 10)
        pdf.setFillColor(colors.grey)
        pdf.drawString(50, 30, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.drawString(width - 150, 30, "© 2025 Trip Management System")

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        response.write(buffer.read())
        buffer.close()
        return response

OPENROUTE_API_KEY = "5b3ce3597851110001cf624837c701f22636484b8007e1f141bda9ef"

def fetch_route_data(start_lat, start_long, end_lat, end_long):
    if not all([start_lat, start_long, end_lat, end_long]):
        print("❌ Error: Missing coordinates in fetch_route_data")
        return None, None  

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {"Authorization": OPENROUTE_API_KEY, "Content-Type": "application/json"}
    data = {"coordinates": [[start_long, start_lat], [end_long, end_lat]]}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        route_data = response.json()

        if "features" not in route_data or not route_data["features"]:
            print("⚠️ No route found in API response")
            return None, None

        segment = route_data["features"][0]["properties"]["segments"][0]
        distance_km = round(segment["distance"] / 1000, 2)
        duration_hours = round(segment["duration"] / 3600, 2)

        print(f"✅ Trip Data: {distance_km} km - {duration_hours} hours")
        return distance_km, duration_hours

    except requests.exceptions.RequestException as e:
        print(f"❌ API request error: {e}")
        return None, None



class TripListCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        trip = serializer.save()

        if not all([trip.current_latitude, trip.current_longitude, trip.dropoff_latitude, trip.dropoff_longitude]):
            print("❌ Error: Incomplete coordinates")
            trip.delete()  
            raise ValueError("Incomplete location data provided")  

        print(f"🚀 Calling OpenRouteService API for trip {trip.id}...")

        estimated_distance_km, estimated_time_hours = fetch_route_data(
            trip.current_latitude, trip.current_longitude,
            trip.dropoff_latitude, trip.dropoff_longitude
        )

        if estimated_time_hours is not None:
            print(f"🔄 Updating cycle_hours_used: {estimated_time_hours} hours")
            trip.cycle_hours_used = estimated_time_hours
            trip.save(update_fields=['cycle_hours_used'])
            trip.refresh_from_db()
            print(f"✅ After save: cycle_hours_used = {trip.cycle_hours_used} hours")

        else:
            print("⚠️ Failed to fetch distance/time data from API")

        return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)



class TripDetailView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        trip = get_object_or_404(Trip, pk=pk)
        trip.delete()
        return Response({"message": "Trip deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, pk, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        if not all([trip.current_latitude, trip.current_longitude, trip.dropoff_latitude, trip.dropoff_longitude]):
            return Response({"error": "Missing latitude/longitude data"}, status=400)

        estimated_distance_km, estimated_time_hours = fetch_route_data(
            trip.current_latitude, trip.current_longitude,
            trip.dropoff_latitude, trip.dropoff_longitude
        )

        if estimated_distance_km is not None and estimated_time_hours is not None:
            trip.cycle_hours_used = estimated_distance_km
            trip.save(update_fields=['cycle_hours_used'])
            trip.refresh_from_db()

        logs = trip.logs.all()
        logs_data = LogEntrySerializer(logs, many=True).data
        total_remaining_hours = sum(log.remaining_hours for log in logs)
        legal_warnings = [log.legal_warning for log in logs if log.legal_warning]

        return Response({
            "trip": TripSerializer(trip).data,
            "logs": logs_data,
            "estimated_time_hours": estimated_time_hours if estimated_time_hours is not None else "N/A",
            "estimated_distance_km": estimated_distance_km if estimated_distance_km is not None else "N/A",
            "total_remaining_hours": total_remaining_hours,
            "warnings": legal_warnings
        })


# ✅ Retrieve trip logs
class TripLogEntriesView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        logs = trip.logs.all()
        serializer = LogEntrySerializer(logs, many=True)
        return Response(serializer.data)
