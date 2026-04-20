import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # 2026'nın en kararlı modeli: gemini-2.0-flash
        # Not: Eğer hata alırsan 'gemini-1.5-flash' da denenebilir ama 2.0 şu an standart.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Sen Şanlıurfa uzmanı Urfamız AI'sın. Samimi bir dille cevap ver. Soru: {user_message}"
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
                return jsonify({"reply": "Şu an cevap veremiyorum, lütfen tekrar dene."})
        else:
            # Hata detayını daha net görelim
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
