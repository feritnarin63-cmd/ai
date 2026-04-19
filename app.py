import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API anahtarını al ve yapılandır
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Hata ihtimalini sıfırlamak için en yalın haliyle modeli tanımla
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Talimatı direkt burada birleştiriyoruz
        full_prompt = f"Sen Şanlıurfa uzmanı 'Urfamız AI'sın. Soru: {user_message}"
        
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Cevap oluşturulamadı, lütfen tekrar dene."})
            
    except Exception as e:
        # Hatayı ekrana bas ki ne olduğunu görelim
        print(f"HATA: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
