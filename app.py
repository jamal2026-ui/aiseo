from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Konfigurasi Gemini API menggunakan Environment Variable dari Render
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=AIzaSyDix5fpgxB_r34nEEZR2Ca1zu8VwiAo8r0)

# Menggunakan model Gemini 1.5 Flash (Gratis & Cepat)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_long_article(title, keywords):
    # LANGKAH 1: Membuat Outline yang sangat detail (8-10 Sub-bab)
    outline_prompt = f"""
    Buatlah outline artikel SEO yang sangat mendalam untuk judul: "{title}".
    Gunakan keyword: {keywords}.
    Berikan daftar 8 sampai 10 judul sub-bab (H2) saja, satu per baris, tanpa angka atau simbol.
    """
    
    outline_response = model.generate_content(outline_prompt)
    outlines = outline_response.text.strip().split('\n')
    
    # Inisialisasi konten dengan Judul Utama
    full_article_html = f"<div class='article-content'><h1>{title}</h1>"

    # LANGKAH 2: Menulis setiap sub-bab secara terpisah (untuk mengejar 1.500+ kata)
    for section in outlines:
        section = section.strip()
        if section:
            print(f"Sedang menulis bagian: {section}")
            
            # Prompt khusus agar Gemini menulis panjang per bagian
            writing_prompt = f"""
            Tuliskan konten artikel yang sangat mendalam dan informatif untuk sub-judul: "{section}".
            Topik utama artikel adalah: "{title}".
            Gunakan keyword: {keywords}.
            
            Instruksi Penulisan:
            1. Tulis minimal 250-300 kata untuk bagian ini saja.
            2. Gunakan gaya bahasa profesional namun mudah dimengerti.
            3. Gunakan format HTML: <p> untuk paragraf, <ul>/<li> jika ada daftar, dan <strong> untuk penekanan kata penting.
            4. Jangan mengulang-ulang kalimat yang sama.
            """
            
            try:
                section_response = model.generate_content(writing_prompt)
                full_article_html += f"<h2>{section}</h2>"
                full_article_html += section_response.text
            except Exception as e:
                full_article_html += f"<h2>{section}</h2><p>Gagal memproses bagian ini: {str(e)}</p>"

    full_article_html += "</div>"
    return full_article_html

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write', methods=['POST'])
def write():
    data = request.json
    title = data.get('title')
    keywords = data.get('keywords')
    
    if not GEMINI_KEY:
        return jsonify({"status": "error", "message": "API Key Gemini belum diset di Render!"})

    try:
        hasil_artikel = generate_long_article(title, keywords)
        return jsonify({"status": "success", "content": hasil_artikel})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
