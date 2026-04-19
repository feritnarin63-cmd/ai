import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API anahtarını al
api_key = os.environ.get("GEMINI_API_KEY")

# ÇOK KRİTİK: Burası v1beta yerine v1 (kararlı) sürümü zorlar
os.environ["GOOGLE_API_USE_MTLS"] = "never" 

genai.configure(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # Modeli bu şekilde (models/ ön ekiyle) çağırmak 404'ü kesebilir
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"Sen Şanlıurfa hakkında uzman bir asistan olan 'Urfamız AI'sın. Soru: {user_message}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Üzgünüm, bir cevap oluşturamadım."})

    except Exception as e:
        # Eğer hala 404 verirse, hata mesajının içinden hangi modellerin 
        # desteklendiğini anlamaya çalışacağız.
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
