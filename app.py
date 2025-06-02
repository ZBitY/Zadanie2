from flask import Flask, render_template_string, request
import logging
import requests
from urllib.parse import quote

AUTHOR_NAME = "Przemek Zbiciak"
TCP_PORT = 5000

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info(f"Aplikacja uruchomiona: Autor: {AUTHOR_NAME}, Port: {TCP_PORT}")

app = Flask(__name__)

locations = {
    "Polska": ["Warszawa", "Krakow", "Gdansk", "Wroclaw", "Lublin"],
    "Niemcy": ["Berlin", "Monachium", "Hamburg", "Frankfurt"],
    "USA": ["New York", "Los Angeles", "Chicago", "Miami", "San Francisco"],
    "Francja": ["Paris", "Lyon", "Marseille"],
    "Wielka Brytania": ["London", "Manchester", "Birmingham"]
}

API_KEY = "9cefd135ae494ef3ad480858252804"

@app.route("/", methods=["GET", "POST"])
def index():
    selected_country = request.form.get("country")
    selected_city = request.form.get("city")
    weather = None

    if selected_country and selected_city:
        city_encoded = quote(selected_city)
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_encoded}&aqi=no"
        try:
            response = requests.get(url)
            if response.ok:
                data = response.json()
                weather = {
                    "time": data["location"]["localtime"].split(" ")[1],
                    "temperature": data["current"]["temp_c"],
                    "description": data["current"]["condition"]["text"],
                    "humidity": data["current"]["humidity"],
                }
            else:
                weather = {"error": f"Nie udało się pobrać pogody.\n{url}"}
        except Exception as e:
            weather = {"error": f"Błąd: {str(e)}"}

    return render_template_string(TEMPLATE, locations=locations, selected_country=selected_country, selected_city=selected_city, weather=weather)

TEMPLATE = """
<!doctype html>
<html lang="pl">
<head><title>Prognoza pogody</title></head>
<body>
    <h1>Wybierz lokalizację</h1>
    <form method="post">
        <label for="country">Kraj:</label>
        <select name="country" id="country" onchange="this.form.submit()">
            <option value="">-- Wybierz kraj --</option>
            {% for country in locations.keys() %}
                <option value="{{ country }}" {% if selected_country == country %}selected{% endif %}>{{ country }}</option>
            {% endfor %}
        </select>
    </form>

    {% if selected_country %}
        <form method="post">
            <input type="hidden" name="country" value="{{ selected_country }}">
            <label for="city">Miasto:</label>
            <select name="city" id="city">
                {% for city in locations[selected_country] %}
                    <option value="{{ city }}" {% if selected_city == city %}selected{% endif %}>{{ city }}</option>
                {% endfor %}
            </select>
            <br>
            <button type="submit">Pokaż pogodę</button>
        </form>
    {% endif %}

    {% if weather %}
        <h2>Pogoda w {{ selected_city }}</h2>
        {% if weather.error %}
            <p>{{ weather.error }}</p>
        {% else %}
            <ul>
                <li>Godzina: {{ weather.time }}</li>
                <li>Temperatura: {{ weather.temperature }} °C</li>
                <li>Opis: {{ weather.description }}</li>
                <li>Wilgotność: {{ weather.humidity }} %</li>
            </ul>
        {% endif %}
    {% endif %}
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=TCP_PORT)
