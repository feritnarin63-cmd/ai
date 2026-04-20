from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Gemini Konfigürasyonu
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# Asistan Kuralları
SYSTEM_CONTEXT = """
Sen urfamiz.com/ai adresindeki resmi yapay zeka asistanısın. 
Şanlıurfa yerel basınına, kültürüne ve güncel olaylara hakimsin.
Cevap verirken urfamiz.com vizyonuyla, tarafsız ve hızlı bilgi sağla.
"""

@app.route('/')
def index():
    # Bu rota urfamiz.com/ai adresine girince çalışır
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message')
    try:
        # Prompt'u sistem bağlamıyla birleştir
        response = model.generate_content(f"{SYSTEM_CONTEXT}\nSoru: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Şu an teknik bir aksaklık yaşıyorum, lütfen Urfamız ekibiyle iletişime geçin."}), 500

if __name__ == "__main__":
    app.run()
