# app.py

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from engine import read_pdf, translate_text, text_to_speech
from summarizer import generate_summary
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'output_audio'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    summary_text = None

    if request.method == 'POST':
        src_lang = request.form['source_lang']
        tgt_lang = request.form['target_lang']
        file = request.files['pdf_file']
        summarize_choice = request.form['summary_mode']

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            full_text = read_pdf(path)
            summary_text = generate_summary(full_text, summarize_choice)
            translated = translate_text(summary_text, src_lang, tgt_lang)
            audio_path = text_to_speech(translated, tgt_lang)
            audio_file = os.path.basename(audio_path)

    return render_template('index.html', audio_file=audio_file, summary=summary_text)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename, as_attachment=True)

@app.route('/output_audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)