import os

def safe_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name)

def try_transcribe_audio(path):
    # placeholder for real AI model
    return f"[Transcript of {os.path.basename(path)}]"

def try_image_caption(path):
    # placeholder for real AI model
    return f"[Caption for {os.path.basename(path)}]"
