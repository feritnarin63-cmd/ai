import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Anahtarını al
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model ayarlarını en stabil hale getirdik
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest" # '-latest' takısı 404 hatalarını çözer
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    # Sistem talimatını prompt içine gömerek hata riskini sıfıra indiriyoruz
    full_prompt = f"Sen Şanlıurfa hakkında uzman bir asistan olan 'Urfamız AI'sın. Soru: {user_message}"
    
    try:
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
