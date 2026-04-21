# Weather API - PM Accelerator Backend Assessment

A RESTful backend API built with Flask that allows users to create, read, update, and delete weather records. This project integrates with an external weather service (Open-Meteo) to fetch real-time weather data based on location and exports data to standard formats.

## 🚀 Features

* **CRUD Operations:** Full Create, Read, Update, and Delete functionality for weather records.
* **External API Integration:** Automatically fetches accurate weather and geolocation data using the Open-Meteo API (no API key required).
* **Data Persistence:** Utilizes SQLite and SQLAlchemy for lightweight, reliable database storage.
* **Data Export:** Download the entire database of weather records in either JSON or CSV format.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** Flask
* **Database:** SQLite
* **ORM:** Flask-SQLAlchemy
* **External API:** Open-Meteo (Geocoding and Weather forecast)

## 📦 Installation & Setup

1. **Clone the repository (Public/Open-Source)**
   ```bash
   git clone <your-github-repo-link>
   cd <your-repo-folder-name>