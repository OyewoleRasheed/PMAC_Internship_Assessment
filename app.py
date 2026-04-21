from flask import Flask, request, jsonify ,  make_response# FIXED: Added request and jsonify
from datetime import datetime
from database import db
from models import WeatherRecord
from weather_service import WeatherService
from export_service import ExportService
import json
import io

app = Flask(__name__)

# CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ==========================================
# CRUD ROUTES
# ==========================================

# 1. CREATE
# Replace your existing CREATE route with this
@app.route('/weather', methods=['POST'])
def create_weather():
    data = request.get_json()
    
    location = data.get('location')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # 1. Basic Validation
    if not location or not start_date or not end_date:
        return jsonify({"error": "Please provide location, start_date, and end_date"}), 400
        
    # 2. Date Range Validation (NEW)
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        if start_dt > end_dt:
            return jsonify({"error": "start_date cannot be after end_date"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD"}), 400

    # 3. Location Validation & API Call
    weather_info = WeatherService.get_weather(location)
    if not weather_info:
        return jsonify({"error": f"Location '{location}' could not be found."}), 404
        
    # Database Persistence
    new_record = WeatherRecord(
        location=location,
        start_date=start_date,
        end_date=end_date,
        weather_data=weather_info
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({"message": "Weather record created successfully", "record": new_record.to_dict()}), 201


# 2. READ (Get all records)
@app.route('/weather', methods=['GET'])
def get_all_weather():
    records = WeatherRecord.query.all()
    return jsonify([record.to_dict() for record in records]), 200

# 2. READ (Get a specific record by ID)
@app.route('/weather/<int:record_id>', methods=['GET'])
def get_weather_by_id(record_id):
    record = WeatherRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record.to_dict()), 200


#  UPDATE route 
@app.route('/weather/<int:record_id>', methods=['PUT'])
def update_weather(record_id):
    record = WeatherRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    data = request.get_json()
    
    # Update Dates with Validation (NEW)
    if 'start_date' in data or 'end_date' in data:
        start_date = data.get('start_date', record.start_date)
        end_date = data.get('end_date', record.end_date)
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if start_dt > end_dt:
                return jsonify({"error": "start_date cannot be after end_date"}), 400
            record.start_date = start_date
            record.end_date = end_date
        except ValueError:
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD"}), 400

    # Update Location with Validation (NEW)
    if 'location' in data and data['location'] != record.location:
        new_location = data['location']
        new_weather = WeatherService.get_weather(new_location)
        if not new_weather:
            return jsonify({"error": f"New location '{new_location}' could not be found."}), 404
        record.location = new_location
        record.weather_data = new_weather
        
    db.session.commit()
    
    return jsonify({"message": "Record updated successfully", "record": record.to_dict()}), 200


# 4. DELETE
@app.route('/weather/<int:record_id>', methods=['DELETE'])
def delete_weather(record_id):
    record = WeatherRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    
    return jsonify({"message": "Record deleted successfully"}), 200

# ==========================================
# REQUIRED INFO ROUTE
# ==========================================
@app.route('/export', methods=['GET'])
def export_data():
    format_type = request.args.get('format', 'json').lower()
    records = WeatherRecord.query.all()
    
    if not records:
        return jsonify({"message": "No data to export"}), 404

    if format_type == 'csv':
        csv_data = ExportService.export_to_csv(records)
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=weather_export.csv"
        response.headers["Content-Type"] = "text/csv"
        return response
        
    # Default to JSON export
    else:
        json_data = [record.to_dict() for record in records]
        response = make_response(json.dumps(json_data, indent=4))
        response.headers["Content-Disposition"] = "attachment; filename=weather_export.json"
        response.headers["Content-Type"] = "application/json"
        return response

# ==========================================
# REQUIRED INFO ROUTE
# ==========================================
@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "developer_name": "Oyewole Rasheed Adebayo",
        "company": "Product Manager Accelerator",
        "description": "Product Manager Accelerator is a premier program designed to help professionals transition into and accelerate their careers in product management, offering mentorship, hands-on projects, and interview preparation."
    }), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)