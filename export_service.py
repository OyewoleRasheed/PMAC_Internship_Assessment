# export_service.py
import csv
import io
import json

class ExportService:
    @staticmethod
    def export_to_csv(records):
        # Create an in-memory string buffer
        si = io.StringIO()
        
        # Define the column headers based on your model
        fieldnames = ['id', 'location', 'start_date', 'end_date', 'weather_data', 'created_at']
        writer = csv.DictWriter(si, fieldnames=fieldnames)
        
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())
            
        # Return the string value of the buffer
        return si.getvalue()