from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/geolocation', methods=['GET'])
def geolocation():
    # Fetch IP-based data from ipapi.co
    ip_info = requests.get("https://ipapi.co/json/").json()

    # Gather additional information from request headers
    data = {
        "ip": ip_info.get("ip"),
        "country": ip_info.get("country_name"),
        "region": ip_info.get("region"),
        "city": ip_info.get("city"),
        "latitude": ip_info.get("latitude"),
        "longitude": ip_info.get("longitude"),
        "postal": ip_info.get("postal"),
        "timezone": ip_info.get("timezone"),
        "as_org": ip_info.get("org"),
        "user_agent": request.headers.get("User-Agent"),
        "language": request.headers.get("Accept-Language"),
        "referrer": request.headers.get("Referer"),
        "session_id": request.headers.get("Session-ID"),
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
