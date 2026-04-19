import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Yapılandırması
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 404 hatasını önlemek için v1beta'yı değil, v1 sürümünü zorlayan en stabil model tanımlama
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Urfa uzmanı talimatı
        prompt = f"Sen Şanlıurfa uzmanı 'Urfamız AI'asistanısın. Soru: {user_message}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Şu an yanıt veremiyorum, lütfen tekrar dene."})
            
    except Exception as e:
        # Hatayı net görmek için loglara yazdır
        print(f"Hata detayı: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
