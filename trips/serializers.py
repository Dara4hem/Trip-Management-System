from rest_framework import serializers
from .models import Trip, LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(source='trip.id', read_only=True)

    class Meta:
        model = LogEntry
        fields = [
            'id', 'trip_id', 'date', 'driving_hours', 'on_duty_hours', 'off_duty_hours',
            'sleeper_berth_hours', 'total_hours', 'remaining_hours', 'legal_warning'
        ]

class TripSerializer(serializers.ModelSerializer):
    logs = LogEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = "__all__"  # ✅ Make sure all fields are serialized


    def validate(self, data):
        if "current_latitude" in data and "current_longitude" in data:
            if not (-90 <= data["current_latitude"] <= 90) or not (-180 <= data["current_longitude"] <= 180):
                raise serializers.ValidationError("❌")

        if "dropoff_latitude" in data and "dropoff_longitude" in data:
            if not (-90 <= data["dropoff_latitude"] <= 90) or not (-180 <= data["dropoff_longitude"] <= 180):
                raise serializers.ValidationError("❌")

        return data
