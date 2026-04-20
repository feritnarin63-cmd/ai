import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Render panelinden gelen API anahtarı
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Ücretsiz kotası en stabil olan model: gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Sen Şanlıurfa uzmanı Urfamız AI'sın. Samimi bir dille Şanlıurfa şivesiyle selamla ve cevap ver. Soru: {user_message}"
                }]
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()

        if response.status_code == 200:
            if 'candidates' in res_data and len(res_data['candidates']) > 0:
                reply = res_data['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"reply": reply})
            else:
                return jsonify({"reply": "Şu an cevap veremiyorum kurban, tekrar dene."})
        else:
            error_msg = res_data.get("error", {}).get("message", "Bilinmeyen hata")
            return jsonify({"error": f"Google Hatası: {error_msg}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Urfamız AI Sunucusu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
