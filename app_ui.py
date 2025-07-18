# app_ui.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pygame
import shutil
import os
from engine import read_pdf, translate_text, text_to_speech

# Root window
root = tk.Tk()
root.title("📘 PDF Translator & Native Audio Book")
root.geometry("700x650")

# Variables
file_path_var = tk.StringVar()
src_lang_var = tk.StringVar(value="auto")
tgt_lang_var = tk.StringVar(value="te")
result_var = tk.StringVar()
save_path_var = tk.StringVar()
is_playing = tk.BooleanVar(value=False)

def upload_file():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        file_path_var.set(path)
        result_var.set("")
        preview_text.delete("1.0", tk.END)
        audio_button.config(state="disabled")
        play_button.config(state="disabled")
        pause_button.config(state="disabled")
        download_button.config(state="disabled")

def perform_translation():
    file_path = file_path_var.get()
    if not file_path:
        messagebox.showwarning("Missing File", "Please upload a PDF first.")
        return
    try:
        raw = read_pdf(file_path)
        translated = translate_text(raw, src_lang_var.get(), tgt_lang_var.get())
        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.END, translated)
        result_var.set("✅ Translation complete! You can now generate audio.")
        audio_button.config(state="normal")
        save_path_var.set("")
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def generate_audio():
    text = preview_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("No Text", "Translate text before generating audio.")
        return
    try:
        audio_path = text_to_speech(text, tgt_lang_var.get())
        result_var.set(f"🎧 Audio ready: {audio_path}")
        save_path_var.set(audio_path)
        play_button.config(state="normal")
        pause_button.config(state="normal")
        download_button.config(state="normal")
    except Exception as e:
        messagebox.showerror("Audio Error", str(e))

def play_audio():
    path = save_path_var.get()
    if path:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        is_playing.set(True)

def pause_audio():
    if is_playing.get():
        pygame.mixer.music.pause()
        is_playing.set(False)
    else:
        pygame.mixer.music.unpause()
        is_playing.set(True)

def download_audio():
    src_path = save_path_var.get()
    if not src_path:
        messagebox.showwarning("No Audio", "Generate audio first.")
        return
    target = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
    if target:
        shutil.copy2(src_path, target)
        messagebox.showinfo("Download Complete", f"Saved to: {target}")

def open_folder():
    os.startfile(os.path.abspath("output_audio"))

# UI Widgets
ttk.Label(root, text="Step 1: Upload PDF").pack(pady=5)
ttk.Button(root, text="📂 Upload PDF", command=upload_file).pack()
ttk.Label(root, textvariable=file_path_var, foreground="gray").pack(pady=3)

ttk.Label(root, text="Step 2: Select Source & Target Languages").pack()
lang_frame = tk.Frame(root)
lang_frame.pack(pady=5)
ttk.Label(lang_frame, text="Source:").grid(row=0, column=0)
ttk.Combobox(lang_frame, textvariable=src_lang_var, values=["auto", "en", "te", "hi", "ta", "ml", "kn", "gu"]).grid(row=0, column=1)
ttk.Label(lang_frame, text="Target:").grid(row=0, column=2)
ttk.Combobox(lang_frame, textvariable=tgt_lang_var, values=["en", "te", "hi", "ta", "ml", "kn", "gu"]).grid(row=0, column=3)

ttk.Button(root, text="🌐 Translate", command=perform_translation).pack(pady=10)
ttk.Label(root, text="Step 3: Preview Translation").pack()
preview_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
preview_text.pack(fill=tk.BOTH, padx=10, pady=5)

audio_button = ttk.Button(root, text="🔊 Generate Audio", command=generate_audio, state="disabled")
audio_button.pack(pady=10)
ttk.Label(root, textvariable=result_var, wraplength=600).pack(pady=5)

play_button = ttk.Button(root, text="▶️ Play", command=play_audio, state="disabled")
pause_button = ttk.Button(root, text="⏸️ Pause/Resume", command=pause_audio, state="disabled")
download_button = ttk.Button(root, text="⬇️ Download Audio", command=download_audio, state="disabled")
open_button = ttk.Button(root, text="📁 Open Audio Folder", command=open_folder, state="disabled")

play_button.pack(pady=2)
pause_button.pack(pady=2)
download_button.pack(pady=2)
open_button.pack(pady=5)

root.mainloop()