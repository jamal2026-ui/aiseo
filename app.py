from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Ganti dengan API Key Anda atau gunakan Environment Variable
openai.api_key = "KODE_API_KEY_ANDA_DI_SINI"

def generate_long_article(title, keywords):
    # Tahap 1: Membuat Outline SEO (H2 & H3)
    outline_prompt = f"Buatlah struktur artikel (H2 saja) sebanyak 8 poin untuk judul: '{title}' dengan fokus keyword: {keywords}. Berikan daftar judulnya saja."
    
    response = openai.ChatCompletion.create(
        model="gpt-4", # Atau gpt-3.5-turbo agar lebih murah
        messages=[{"role": "user", "content": outline_prompt}]
    )
    
    outlines = response.choices[0].message.content.strip().split('\n')
    full_article_html = f"<h1>{title}</h1>"

    # Tahap 2: Menulis isi per sub-judul (looping untuk mencapai 1.500+ kata)
    for section in outlines:
        if section.strip():
            print(f"Sedang menulis bagian: {section}")
            content_prompt = f"Tulis artikel mendalam (minimal 250 kata) untuk sub-bab: '{section}'. Topik utama: {title}. Gunakan keyword: {keywords}. Gunakan format HTML <p> dan jika perlu <ul>."
            
            section_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": content_prompt}]
            )
            
            full_article_html += f"<h2>{section}</h2>"
            full_article_html += section_response.choices[0].message.content

    return full_article_html

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/write', methods=['POST'])
def write():
    data = request.json
    try:
        hasil = generate_long_article(data['title'], data['keywords'])
        return jsonify({"status": "success", "content": hasil})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)