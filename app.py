from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b4088d5e99954b00a64184705261406"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    city = request.form["city"]

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=14&aqi=yes&alerts=yes"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "error" in data:
            return data["error"]["message"]

        current = data["current"]
        location = data["location"]
        forecast = data["forecast"]["forecastday"]
        hourly_data = forecast[0]["hour"]

        temperature = current["temp_c"]
        condition = current["condition"]["text"]
        weather_class = condition.lower().replace(" ", "-")

        aqi = current.get("air_quality", {}).get("us-epa-index", "N/A")

        if temperature > 40:
            alert = "🔥 Heatwave Warning: Avoid going outside in afternoon."
        elif current["uv"] > 8:
            alert = "☀ High UV Alert: Use sunscreen and avoid direct sunlight."
        elif aqi != "N/A" and aqi > 150:
            alert = "😷 Poor Air Quality: Wear a mask outside."
        elif "rain" in condition.lower():
            alert = "☔ Rain Alert: Carry an umbrella."
        else:
            alert = "✅ Weather looks normal today."

        if temperature > 35:
            advice = "🥤 Stay hydrated and avoid direct sunlight."
        elif temperature < 10:
            advice = "🧥 Wear warm clothes."
        elif "rain" in condition.lower():
            advice = "☔ Carry an umbrella. Rain chances are high."
        else:
            advice = "🌤 Great weather for outdoor activities."

        return render_template(
            "result.html",
            city=location["name"],
            region=location["region"],
            country=location["country"],
            temperature=current["temp_c"],
            feelslike=current["feelslike_c"],
            humidity=current["humidity"],
            wind_speed=current["wind_kph"],
            wind_dir=current["wind_dir"],
            gust=current["gust_kph"],
            pressure=current["pressure_mb"],
            visibility=current["vis_km"],
            uv=current["uv"],
            cloud=current["cloud"],
            precip=current["precip_mm"],
            condition=condition,
            icon=current["condition"]["icon"],
            weather_main=condition,
            weather_class=weather_class,
            sunrise=forecast[0]["astro"]["sunrise"],
            sunset=forecast[0]["astro"]["sunset"],
            chance_of_rain=forecast[0]["day"]["daily_chance_of_rain"],
            max_temp=forecast[0]["day"]["maxtemp_c"],
            min_temp=forecast[0]["day"]["mintemp_c"],
            aqi=aqi,
            alert=alert,
            advice=advice,
            insight1="Best time for outdoor activity: Evening",
            insight2="Travel risk: Low",
            insight3="Comfort score: 8.5 / 10",
            forecast=forecast,
            hourly_data=hourly_data
        )

    except Exception as e:
        return f"Error: {e}"


@app.route("/search_city")
def search_city():
    query = request.args.get("q")

    if not query:
        return []

    url = f"http://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}"

    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception:
        return []


if __name__ == "__main__":
    app.run(debug=True)