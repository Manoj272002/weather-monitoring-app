# Weather Monitoring App
This project is a real-time weather monitoring application built with Flask. It fetches and stores weather data for multiple cities, calculates daily summaries, and triggers alerts when certain temperature or weather conditions are met.

Project Overview The application collects data from the OpenWeatherMap API and stores it in an SQLite database. It runs periodic checks on the weather data, provides daily summaries, and raises alerts for user-defined conditions like temperature thresholds or specific weather events.

Key Features Real-time weather data collection for multiple cities Configurable alert thresholds (e.g., temperature and specific weather conditions) Daily weather summaries with average, max, min temperatures, and dominant weather condition A simple web interface for viewing summaries and alerts

README: Detailed documentation on building, setting up, and running the application with design insights Dependencies Flask: Web framework to build and manage the application. requests: Used for making HTTP requests to the OpenWeatherMap API. sqlite3: Local database for storing weather data and daily summaries.

Environment Setup: Update your OpenWeatherMap API key in app.py: API_KEY = "your_openweathermap_api_key" Run the Application: Start the Flask server and background threads for data fetching and summary calculation: python app.py Access the Application: Once running, access the application on http://localhost:5000 in your browser.

Design Choices: Database: SQLite was chosen for its simplicity and easy local setup. This allows the project to be run locally without complex database configuration. Multithreading: Threads are used to handle continuous weather data fetching and daily summary calculations independently of the Flask request/response cycle. Configurable Thresholds: The application includes configurable thresholds, making it adaptable to different weather conditions or cities.
