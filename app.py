from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Sitenin farklı bir domain/port üzerinden erişebilmesi için

# 1. Gemini API Yapılandırması
# API anahtarını doğrudan yazabilir veya ortam değişkeni kullanabilirsin
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Asistanın Kişiliği (System Instruction)
SYSTEM_PROMPT = """
Sen urfamiz.com sitesinin resmi yapay zeka asistanısın. 
Görevlerin:
- Şanlıurfa hakkında tarih, kültür ve güncel haber bilgisi vermek.
- Kullanıcılara samimi, yerel kültüre saygılı ve yardımsever bir dille cevap vermek.
- Eğer bilmediğin bir haber varsa 'Sitemizdeki güncel haberleri kontrol ediyorum' diyerek geçiştirme, 
mevcut genel bilginle yardımcı ol.
- Cevaplarını kısa ve öz tut, kullanıcıyı yorma.
"""

@app.route('/ask', methods=['POST'])
def ask_ai():
    try:
        user_data = request.json
        user_question = user_data.get('question')

        if not user_question:
            return jsonify({"error": "Soru boş olamaz"}), 400

        # Modeli çalıştır
        chat = model.start_chat(history=[])
        full_prompt = f"{SYSTEM_PROMPT}\n\nKullanıcı: {user_question}"
        
        response = chat.send_message(full_prompt)
        
        return jsonify({
            "status": "success",
            "answer": response.text
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Localde test etmek için 5000 portunda çalışır
    app.run(debug=True, port=5000)
