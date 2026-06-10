import os
from flask import Flask, request, jsonify 
import requests

app = Flask(__name__)

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "https://api.google.com/gemini")

APPROVED_PROVIDERS = [
    "European CDC",
    "WHO",
    "Mayo Clinic",
    "Cleveland Clinic",
    "Johns Hopkins Medicine",
    "Health Canada",
    "Santé Québec"
]

@app.route('data/raw/health-data', methods=['POST'])
def receive_health_data():
    health_data = request.json or {}
    recommendations = process_health_data(health_data)
    return jsonify(recommendations), 200

def build_gemini_payload(data):
    approved_list = ", ".join(APPROVED_PROVIDERS)
    return {
        "prompt": {
            "system": (
                "You are a health analytics assistant. Analyze Apple Health data and return "
                "structured recommendations. Only use data from approved providers: "
                f"{approved_list}. Output JSON with keys: summary, recommendations, flags, "
                "and warnings. Focus on sleep, activity, heart rate, recovery, and any "
                "anomalies. If a value is missing, note that it was not provided."
            ),
            "user": (
                "Analyze the following health record and produce concise, actionable guidance:\n\n"
                f"{data}"
            )
        },
        "temperature": 0.0,
        "max_output_tokens": 1024
    }

def interact_with_gemini(data):
    if not CLAUDE_API_KEY:
        return {"status": "error", "message": "Missing GEMINI_API_KEY environment variable."}

    payload = build_gemini_payload(data)
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=15)

    if response.ok:
        return response.json()
    return {
        "status": "error",
        "message": f"Gemini request failed with status {response.status_code}",
        "detail": response.text,
    }

def process_health_data(data):
    return interact_with_gemini(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)