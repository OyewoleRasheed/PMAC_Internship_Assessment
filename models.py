# models.py
from database import db
from datetime import datetime

class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    
    # Store the returned weather data (temperature, etc.) as a JSON string or text
    weather_data = db.Column(db.Text, nullable=True) 
    
    # Keep track of when the user made this search
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        # A helper method to easily convert the database row into a JSON-friendly dictionary
        return {
            "id": self.id,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "weather_data": self.weather_data,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }