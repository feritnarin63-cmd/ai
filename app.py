import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API anahtarını yapılandır
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        
        # 404 HATASINI ÇÖZEN KRİTİK SATIR: 
        # Modeli metodun içinde, tam ismiyle çağırıyoruz.
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Sen Şanlıurfa hakkında uzman bir asistan olan 'Urfamız AI'sın. Soru: {user_message}"
        
        # Cevap üretme
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": response.text})
        else:
            return jsonify({"reply": "Üzgünüm, şu an cevap üretemedim."})

    except Exception as e:
        error_msg = str(e)
        print(f"HATA DETAYI: {error_msg}")
        # Eğer hala 404 verirse alternatif model ismini dene mesajı
        return jsonify({"error": error_msg}), 500

@app.route('/')
def home():
    return "Sunucu Aktif!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
