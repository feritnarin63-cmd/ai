import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Anahtarını çek
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 404 hatasını geçmek için en standart model ismini kullanıyoruz
model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # Talimatı direkt burada veriyoruz ki hata payı kalmasın
    prompt = f"Sen Şanlıurfa hakkında uzman bir yapay zeka asistanısın. İsmim Ferit. Soru: {user_message}"
    
    try:
        response = model.generate_content(prompt)
        # Cevabın boş gelme ihtimaline karşı kontrol
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Üzgünüm, şu an cevap üretemedim."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
