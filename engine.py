# engine.py

from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from gtts import gTTS
from datetime import datetime
import os
import re

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def clean_text(text):
    text = re.sub(r'[“”"\']', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def translate_text(text, src_lang='auto', dest_lang='te'):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    return translator.translate(text)

def create_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def ensure_output_dir():
    dir_path = "output_audio"
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def text_to_speech(text, language='te'):
    cleaned = clean_text(text)
    filename = f"book_audio_{create_timestamp()}.mp3"
    out_path = os.path.join(ensure_output_dir(), filename)
    tts = gTTS(text=cleaned, lang=language)
    tts.save(out_path)
    return out_path