from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from gtts import gTTS
from datetime import datetime
import os

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def translate_text(text, dest_language='te'):
    translator = GoogleTranslator(source='auto', target=dest_language)
    translated = translator.translate(text)
    return translated

def create_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def ensure_output_dir():
    dir_path = "output_audio"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def text_to_speech(text, filename, language='te'):
    tts = gTTS(text=text, lang=language)
    output_dir = ensure_output_dir()
    filepath = os.path.join(output_dir, filename + ".mp3")
    tts.save(filepath)
    return filepath

def process_book(pdf_path, lang='te'):
    print("📖 Reading PDF...")
    text = read_pdf(pdf_path)

    print("🌐 Translating to native language...")
    translated_text = translate_text(text, dest_language=lang)

    print("🔊 Generating audio...")
    timestamp = create_timestamp()
    filename = f"book_audio_{timestamp}"
    audio_file = text_to_speech(translated_text, filename, language=lang)

    print(f"✅ Audio saved at: {audio_file}")

if __name__ == "__main__":
    pdf_path = "C:\\Users\\prave\\Documents\\Python_projects\\BookReader\\sample.pdf"
    process_book(pdf_path, lang='te')