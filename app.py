import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API anahtarını al
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Modeli en garanti şekilde tanımlıyoruz
model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")
        
        # Urfa uzmanı talimatını buraya ekliyoruz
        prompt = f"Sen Şanlıurfa hakkında uzman bir asistan olan 'Urfamız AI'sın. Soru: {user_input}"
        
        # Stream=False yaparak tam yanıtın gelmesini bekliyoruz
        response = model.generate_content(prompt)
        
        return jsonify({"reply": response.text})
    except Exception as e:
        # Hata detayını Render loglarına yazdırır
        print(f"Hata detayı: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
