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
        
        # Google'ın ham API adresi (v1 sürümü zorlamalı)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Sen Şanlıurfa uzmanı Urfamız AI'sın. Soru: {user_message}"
                }]
            }]
        }

        # İsteği gönderiyoruz
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()

        # Yanıtı kontrol et
        if response.status_code == 200:
            # Google'dan gelen karmaşık JSON içinden cevabı çekiyoruz
            reply = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": reply})
        else:
            # Hata varsa ne olduğunu tam olarak görelim
            error_detail = res_data.get("error", {}).get("message", "Bilinmeyen hata")
            return jsonify({"error": f"Google Hatası: {error_detail}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Urfamız AI Sunucusu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
