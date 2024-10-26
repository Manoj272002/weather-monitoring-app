app.py - Main Application Code

from flask import Flask, render_template, jsonify, request
from threading import Thread
import requests
import sqlite3
import time
from datetime import datetime
from collections import Counter

app = Flask(__name__)

API_KEY = "c7d64e40bcf89ba40805da20d18d07f9"  # Replace with your actual API key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
FETCH_INTERVAL = 300  # 5 minutes
ALERT_TEMP_THRESHOLD = 35  # Celsius
ALERT_CONDITION_THRESHOLD = "Rain"

conn = sqlite3.connect('weather_data.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY,
                    city TEXT,
                    main TEXT,
                    temp REAL,
                    feels_like REAL,
                    dt INTEGER,
                    timestamp TEXT
                  )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
                    city TEXT,
                    date TEXT,
                    avg_temp REAL,
                    max_temp REAL,
                    min_temp REAL,
                    dominant_condition TEXT,
                    UNIQUE(city, date)
                  )''')
conn.commit()

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 2)

def fetch_weather_data():
    while True:
        for city in CITIES:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                main = data['weather'][0]['main']
                temp = kelvin_to_celsius(data['main']['temp'])
                feels_like = kelvin_to_celsius(data['main']['feels_like'])
                dt = data['dt']
                timestamp = datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''INSERT INTO weather (city, main, temp, feels_like, dt, timestamp)
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (city, main, temp, feels_like, dt, timestamp))
                conn.commit()
                check_alerts(city, temp, main)
        time.sleep(FETCH_INTERVAL)

def check_alerts(city, temp, condition):
    if temp > ALERT_TEMP_THRESHOLD:
        print(f"Alert: {city} temperature exceeded {ALERT_TEMP_THRESHOLD}°C with {temp}°C")
    if condition == ALERT_CONDITION_THRESHOLD:
        print(f"Alert: {city} has {ALERT_CONDITION_THRESHOLD} condition.")

def calculate_daily_summaries():
    while True:
        today = datetime.now().strftime('%Y-%m-%d')
        for city in CITIES:
            cursor.execute('''SELECT temp, main FROM weather WHERE city=? AND date(timestamp)=?''', (city, today))
            results = cursor.fetchall()
            if results:
                temps = [r[0] for r in results]
                conditions = [r[1] for r in results]
                avg_temp = round(sum(temps) / len(temps), 2)
                max_temp = max(temps)
                min_temp = min(temps)
                dominant_condition = Counter(conditions).most_common(1)[0][0]

                cursor.execute('''INSERT OR IGNORE INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (city, today, avg_temp, max_temp, min_temp, dominant_condition))
                conn.commit()
        time.sleep(86400)  # Update daily

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/daily_summary')
def daily_summary():
    summaries = {}
    for city in CITIES:
        cursor.execute('''SELECT * FROM daily_summary WHERE city=? ORDER BY date DESC LIMIT 1''', (city,))
        summaries[city] = cursor.fetchone()
    return render_template("daily_summary.html", summaries=summaries)

@app.route('/alerts')
def alerts():
    return render_template("alerts.html")

weather_thread = Thread(target=fetch_weather_data)
summary_thread = Thread(target=calculate_daily_summaries)
weather_thread.start()
summary_thread.start()

def run_app():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = Thread(target=run_app)
flask_thread.start()
